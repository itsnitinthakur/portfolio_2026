# portfolio/management/commands/seed_portfolio.py
"""
Load the site owner's details from portfolio/seed_data.py into the database.

    python manage.py seed_portfolio            # add anything that is missing
    python manage.py seed_portfolio --update   # also overwrite existing rows

Safe to run as often as you like: rows are matched, never duplicated.
"""

from datetime import date
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from portfolio import seed_data
from portfolio.models import Company, Education, Experience, Product, Profile, Project, Skill

SEED_ASSETS = Path(__file__).resolve().parents[2] / "seed_assets"
PROFILE_PHOTO = SEED_ASSETS / "profile.jpg"


def parse_date(value):
    return date.fromisoformat(value) if value else None


class Command(BaseCommand):
    help = "Load profile, company, products, skills, experience, projects and education from portfolio/seed_data.py."

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            help=(
                "Overwrite rows that already exist with the values in seed_data.py. "
                "Without this flag, existing rows are left exactly as they are."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.update = options["update"]
        self.counts = {"created": 0, "updated": 0, "kept": 0}
        self.notes = []

        profile = self.seed_profile()
        skills = self.seed_skills()
        experiences = self.seed_experiences(skills)
        self.seed_projects(skills, experiences)
        self.seed_education()
        self.seed_company()

        if not profile.email:
            self.notes.append(
                "Profile has no contact email: set PORTFOLIO_CONTACT_EMAIL and run "
                "again with --update, or add it in the admin."
            )
        self.stdout.write(
            self.style.SUCCESS(
                "Portfolio data loaded: {created} created, {updated} updated, "
                "{kept} already present and left as they were.".format(**self.counts)
            )
        )
        for note in self.notes:
            self.stdout.write(self.style.WARNING(f"  ! {note}"))

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def upsert(self, model, lookup, values):
        """
        Create the row if it is missing; overwrite it only with --update.
        Returns (object, changed).
        """
        obj = model.objects.filter(**lookup).first()
        created = obj is None
        if created:
            obj = model(**lookup)
        elif not self.update:
            self.counts["kept"] += 1
            return obj, False

        for field, value in values.items():
            setattr(obj, field, value)
        try:
            obj.full_clean()
        except ValidationError as error:
            raise CommandError(f"{model.__name__} {lookup}: {error.message_dict}") from error
        obj.save()
        self.counts["created" if created else "updated"] += 1
        return obj, True

    def pick_skills(self, names, skills, owner):
        try:
            return [skills[name] for name in names]
        except KeyError as error:
            raise CommandError(
                f"{owner} lists the skill {error.args[0]!r}, which is not in SKILLS."
            ) from error

    # ------------------------------------------------------------------ #
    # Sections
    # ------------------------------------------------------------------ #
    def seed_profile(self):
        values = dict(seed_data.PROFILE)
        if Profile.load() is not None:
            # Blank seed values never wipe details typed into the admin.
            values = {field: value for field, value in values.items() if value}
        profile, _ = self.upsert(Profile, {"pk": 1}, values)

        if PROFILE_PHOTO.exists() and not profile.photo:
            with PROFILE_PHOTO.open("rb") as handle:
                profile.photo.save("profile.jpg", File(handle), save=True)
        return profile

    def seed_skills(self):
        skills = {}
        for position, entry in enumerate(seed_data.SKILLS):
            skill, _ = self.upsert(
                Skill,
                {"name": entry["name"]},
                {
                    "category": entry["category"],
                    "level": entry["level"],
                    "is_featured": entry.get("is_featured", False),
                    "order": position,
                },
            )
            skills[skill.name] = skill
        return skills

    def seed_experiences(self, skills):
        experiences = {}
        for entry in seed_data.EXPERIENCES:
            company = entry["company"]
            missing = [key for key in ("job_title", "start_date") if not entry.get(key)]
            if missing:
                existing = Experience.objects.filter(company=company).first()
                if existing is None:
                    self.notes.append(
                        f"Experience at {company} skipped: fill in "
                        f"{' and '.join(missing)} in seed_data.py."
                    )
                else:
                    experiences[company] = existing
                    self.counts["kept"] += 1
                continue

            experience, changed = self.upsert(
                Experience,
                {"company": company},
                {
                    "job_title": entry["job_title"],
                    "company_url": entry.get("company_url", ""),
                    "location": entry.get("location", ""),
                    "employment_type": entry.get("employment_type", "full_time"),
                    "start_date": parse_date(entry["start_date"]),
                    "end_date": parse_date(entry.get("end_date")),
                    "summary": entry.get("summary", ""),
                    "highlights": "\n".join(entry.get("highlights", [])),
                    "is_published": entry.get("is_published", True),
                },
            )
            if changed:
                experience.skills.set(
                    self.pick_skills(entry.get("skills", []), skills, f"Experience at {company}")
                )
            experiences[company] = experience
        return experiences

    def seed_projects(self, skills, experiences):
        for position, entry in enumerate(seed_data.PROJECTS):
            title = entry["title"]
            experience = experiences.get(entry.get("company"))
            project, changed = self.upsert(
                Project,
                {"slug": slugify(title)},
                {
                    "title": title,
                    "summary": entry["summary"],
                    "description": entry["description"],
                    "impact": entry.get("impact", ""),
                    "role": entry.get("role", ""),
                    "experience": experience,
                    "status": entry.get("status", "completed"),
                    "github_url": entry.get("github_url", ""),
                    "live_url": entry.get("live_url", ""),
                    "cover_image_alt": entry.get("cover_image_alt", ""),
                    "is_featured": entry.get("is_featured", False),
                    "is_published": entry.get("is_published", True),
                    "order": position,
                },
            )
            if changed:
                project.skills.set(
                    self.pick_skills(entry.get("skills", []), skills, f"Project {title!r}")
                )
            elif project.experience is None and experience is not None:
                # The role was added after the project: link them now.
                project.experience = experience
                project.save(update_fields=["experience", "updated_at"])
            self.attach_cover(project, entry)

    def attach_cover(self, project, entry):
        filename = entry.get("cover_image")
        if not filename or project.cover_image:
            return
        path = SEED_ASSETS / filename
        if not path.exists():
            self.notes.append(f"Cover image {filename} for {project.title!r} not found in seed_assets.")
            return
        with path.open("rb") as handle:
            project.cover_image.save(f"{project.slug}{path.suffix}", File(handle), save=False)
        project.cover_image_alt = project.cover_image_alt or entry.get("cover_image_alt", "")
        project.save(update_fields=["cover_image", "cover_image_alt", "updated_at"])

    def seed_education(self):
        for position, entry in enumerate(seed_data.EDUCATION):
            self.upsert(
                Education,
                {"institution": entry["institution"], "qualification": entry["qualification"]},
                {
                    "field_of_study": entry.get("field_of_study", ""),
                    "location": entry.get("location", ""),
                    "start_year": entry.get("start_year"),
                    "end_year": entry.get("end_year"),
                    "honours": entry.get("honours", ""),
                    "description": entry.get("description", ""),
                    "order": position,
                    "is_published": entry.get("is_published", True),
                },
            )

    def seed_company(self):
        data = dict(seed_data.COMPANY)
        for key in ("capabilities", "clients", "offices"):
            data[key] = "\n".join(data.get(key, []))
        if Company.load() is not None:
            data = {field: value for field, value in data.items() if value not in ("", None)}
        company, _ = self.upsert(Company, {"pk": 1}, data)

        for position, entry in enumerate(seed_data.PRODUCTS):
            self.upsert(
                Product,
                {"company": company, "name": entry["name"]},
                {
                    "category": entry["category"],
                    "summary": entry.get("summary", ""),
                    "url": entry.get("url", seed_data.PRODUCTS_URL),
                    "is_featured": entry.get("is_featured", False),
                    "is_published": entry.get("is_published", True),
                    "order": position,
                },
            )
