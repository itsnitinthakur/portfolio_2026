# Deploying the portfolio for free (GitHub + PythonAnywhere)

GitHub Pages only serves static HTML, so it cannot run Django. The plan is:

- **GitHub** stores your code.
- **PythonAnywhere** (free "Beginner" account) runs the site at `https://USERNAME.pythonanywhere.com`.

The free plan has a few limits:

- **One web app.** The address is `USERNAME.pythonanywhere.com`; a custom domain needs a paid plan.
- **About 512 MB of disk.**
- **Limited daily CPU for consoles.** If `pip install` is slow, that's why. The website itself keeps working.
- **The web app must be renewed every month.** Click **"Run until 1 month from today"** on the Web tab. PythonAnywhere emails you before it expires.
- **Outbound internet is restricted.** Contact-form emails may not send, but every message is still saved in the admin.

Throughout this guide, replace `USERNAME` with your PythonAnywhere username and
`GITHUB_USER` with `itsnitinthakur`.

---

## Part 1: Put the code on GitHub (on your Mac)

1. On github.com, click **New repository**.
   - **Name:** `portfolio-site`.
   - **Visibility:** Public is fine. The `.env` file with your secrets is never uploaded, because `.gitignore` excludes it.
   - Leave "Add a README" **unticked**.

2. In Terminal, inside the `portfolio_site` folder:

   ```bash
   git init
   git add .
   git commit -m "Portfolio site"
   git branch -M main
   git remote add origin https://github.com/GITHUB_USER/portfolio-site.git
   git push -u origin main
   ```

3. Before you push, run `git status`. `.env`, `db.sqlite3` and `media/` must **not** be listed. If one is, stop and check `.gitignore`.

When GitHub asks for a password, use a personal access token
(GitHub → Settings → Developer settings → Personal access tokens), not your account password.

---

## Part 2: Set up PythonAnywhere

### 2.1 Create the account

Sign up at https://www.pythonanywhere.com/ and choose the free **Beginner** account.
The username you pick becomes your web address.

### 2.2 Get the code and install it

Open **Consoles → Bash**, then run:

```bash
git clone https://github.com/GITHUB_USER/portfolio-site.git
cd portfolio-site
mkvirtualenv --python=python3.12 portfolio
pip install -r requirements.txt
```

You'll see `(portfolio)` at the start of the prompt while the virtualenv is active.
In a new console, run `workon portfolio` to activate it again.

### 2.3 Create the server's `.env`

Still in the console, generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

Then create the file with `nano .env` and paste this, replacing the values:

```ini
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=paste-the-generated-key-here
DJANGO_ALLOWED_HOSTS=USERNAME.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://USERNAME.pythonanywhere.com
DJANGO_SECURE_SSL_REDIRECT=False
PORTFOLIO_CONTACT_EMAIL=your-kamtronics-address@example.com
```

Save with `Ctrl+O`, `Enter`, `Ctrl+X`. HTTPS is switched on in the Web tab
(step 2.5), which is why `DJANGO_SECURE_SSL_REDIRECT` is `False` here.

### 2.4 Build the database

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_portfolio
python manage.py createsuperuser
```

### 2.5 Create the web app

1. Open the **Web** tab and click **Add a new web app**.
2. Click **Next**, choose **Manual configuration** (not "Django"), then **Python 3.12**.
3. On the web app page, set these:

| Setting | Value |
|---|---|
| Source code | `/home/USERNAME/portfolio-site` |
| Working directory | `/home/USERNAME/portfolio-site` |
| Virtualenv | `/home/USERNAME/.virtualenvs/portfolio` |

4. Click the **WSGI configuration file** link. Delete everything in it, paste the contents of
   `deploy/pythonanywhere_wsgi.py`, change `USERNAME`, and click **Save**.

5. Under **Static files**, add two entries:

| URL | Directory |
|---|---|
| `/static/` | `/home/USERNAME/portfolio-site/staticfiles` |
| `/media/` | `/home/USERNAME/portfolio-site/media` |

6. Under **Security**, turn on **Force HTTPS**.
7. Click the green **Reload** button at the top.

Open `https://USERNAME.pythonanywhere.com`. The admin is at `/admin/`.

---

## Part 3: Updating the live site

On your Mac, make changes, then commit and push:

```bash
git add .
git commit -m "Describe the change"
git push
```

Then in a PythonAnywhere Bash console:

```bash
cd ~/portfolio-site
workon portfolio
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Finally, click **Reload** on the Web tab.

Content you add in the admin, such as projects, product photos and contact messages,
lives only in the server's database. It isn't in GitHub. Download a backup now and then
from the **Files** tab: `db.sqlite3` and the `media/` folder.

---

## If something goes wrong

| What you see | Fix |
|---|---|
| "Something went wrong" page | Web tab → **Error log**. The last lines show the real error. |
| `DisallowedHost` / Bad Request (400) | `DJANGO_ALLOWED_HOSTS` in `.env` must be exactly `USERNAME.pythonanywhere.com`. Reload. |
| Admin or contact form says "CSRF verification failed" | `DJANGO_CSRF_TRUSTED_ORIGINS` must be `https://USERNAME.pythonanywhere.com`. Reload. |
| Page has no styling | The Tailwind CDN is blocked by your network, or `collectstatic` was not run (admin unstyled). |
| Photos missing | Check the `/media/` static-files mapping, then Reload. |
| `ImproperlyConfigured: Set DJANGO_SECRET_KEY` | `.env` is missing or not in `/home/USERNAME/portfolio-site`. |
| Site offline after a month | Web tab → **Run until 1 month from today**. |
