# Portfolio website (Django 5.2 + Tailwind CSS)

A mobile-first portfolio site: home page, experience timeline with education,
projects with skill filters, a Machines page for the company you represent
(with "ask about this machine" links), a skills page, and a contact form that
saves enquiries to an admin inbox. All content is edited in the Django admin.

## Run it on your computer (localhost)

You need **Python 3.10 – 3.13**. Check with `python3 --version`.

### macOS / Linux

```bash
cd portfolio_site
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
python manage.py runserver
```

### Windows (PowerShell)

```powershell
cd portfolio_site
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
python manage.py runserver
```

Then open:

- Website: http://127.0.0.1:8000/
- Admin (edit everything): http://127.0.0.1:8000/admin/

Stop the server with `Ctrl+C`. Next time you only need to activate the virtual
environment (`source .venv/bin/activate`) and run `python manage.py runserver`.

### Check it on your phone

Your phone must be on the same Wi-Fi.

1. Find your computer's local IP. On a Mac: `ipconfig getifaddr en0`. On Windows: `ipconfig`, then look for the IPv4 address.
2. In `.env`, add that IP to the allowed hosts, for example `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.25`.
3. Run `python manage.py runserver 0.0.0.0:8000`.
4. On your phone, open `http://192.168.1.25:8000`.

## Updating from the previous version

If you already ran the earlier version, keep your `.env`, `db.sqlite3` and `media/`
folder, and replace everything else with the new files. Then:

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py seed_portfolio --update
python manage.py runserver
```

`--update` overwrites the seeded rows with the new content. Anything you only
added in the admin, and is not in `seed_data.py`, is left alone.

## Editing content

- **Admin:** change anything at `/admin/`. The sections are Profile, Company (with its products), Products, Skills, Experience, Education, Projects and Contact messages.
- **Seed file:** `portfolio/seed_data.py` holds the starting content. After editing it, run `python manage.py seed_portfolio --update`. Without `--update`, rows that already exist are never overwritten.
- **Projects:** add them in the admin under *Projects*, with a cover image, skills and links. Featured projects appear on the home page.
- **Contact messages:** they arrive under *Contact messages*. Opening one marks it read, and the "Reply by email" button opens your mail app.

## Run the tests

```bash
python manage.py test portfolio
```

## Project structure

```
portfolio_site/
├── manage.py
├── requirements.txt
├── .env.example            copy to .env (never commit .env)
├── .gitignore
├── config/                 project settings and root URLs
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/              site-wide 404 and 500 pages
└── portfolio/              the app
    ├── models.py           Profile, Company, Product, Skill, Experience, Education, Project, ContactMessage
    ├── admin.py
    ├── views.py            class-based views
    ├── urls.py
    ├── forms.py            contact form with spam honeypot
    ├── context_processors.py
    ├── seed_data.py        starting content
    ├── seed_assets/        profile photo and project covers loaded by the seed command
    ├── management/commands/seed_portfolio.py
    ├── migrations/
    ├── static/portfolio/js/site.js   mobile menu
    ├── templates/portfolio/          pages and partials
    └── tests.py
```

## Before going live

- Set `DJANGO_DEBUG=False`, a real `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Run `python manage.py collectstatic`. WhiteNoise then serves the static files.
- Uploaded images in `media/` need persistent storage on your host.
- Replace the Tailwind Play CDN `<script>` in `base.html` with a compiled stylesheet. The CDN is for development only.
- GitHub Pages cannot run Django because it only hosts static files. The code can live on GitHub, but the site needs a Python host.
