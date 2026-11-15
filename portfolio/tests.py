# portfolio/tests.py
"""Run with:  python manage.py test"""

import datetime as dt
import shutil
import tempfile
from io import StringIO

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.html import escape

from .models import ContactMessage, Experience, Profile, Project, Skill


TEST_MEDIA = tempfile.mkdtemp(prefix="portfolio-test-media-")


def tearDownModule():
    shutil.rmtree(TEST_MEDIA, ignore_errors=True)


@override_settings(MEDIA_ROOT=TEST_MEDIA)
class SeededSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_portfolio", stdout=StringIO())

    def test_public_pages_load(self):
        for name in ("home", "experience", "project_list", "skills", "contact"):
            with self.subTest(page=name):
                response = self.client.get(reverse(f"portfolio:{name}"))
                self.assertEqual(response.status_code, 200)

    def test_home_shows_profile_and_current_role(self):
        response = self.client.get(reverse("portfolio:home"))
        profile = Profile.load()
        self.assertContains(response, escape(profile.headline))
        current = Experience.objects.current().first()
        self.assertContains(response, escape(current.job_title))

    def test_mobile_menu_markup(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, 'aria-controls="mobile-menu"')
        self.assertContains(response, 'aria-expanded="false"')
        self.assertContains(response, 'name="viewport"')


class ProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.python = Skill.objects.create(name="Python")
        cls.live = Project.objects.create(title="Live One", summary="s", description="d")
        cls.live.skills.add(cls.python)
        cls.hidden = Project.objects.create(title="Hidden", summary="s", description="d", is_published=False)

    def test_detail_and_unpublished_404(self):
        self.assertEqual(self.client.get(self.live.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)

    def test_skill_filter(self):
        response = self.client.get(reverse("portfolio:project_list"), {"skill": "python"})
        self.assertContains(response, "Live One")
        self.assertNotContains(response, "Hidden")
        self.assertEqual(
            self.client.get(reverse("portfolio:project_list"), {"skill": "nope"}).status_code, 404
        )


@override_settings(CONTACT_NOTIFY_EMAIL="owner@example.com")
class ContactTests(TestCase):
    data = {
        "name": "Li Wei",
        "email": "li@example.com",
        "inquiry_type": "supplier",
        "subject": "Sensors",
        "message": "We make conveyor sensors and would like to talk.",
    }

    def test_valid_message_saved_and_emailed(self):
        response = self.client.post(reverse("portfolio:contact"), self.data, follow=True)
        self.assertContains(response, "your message has been sent")
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_honeypot_is_not_saved(self):
        self.client.post(reverse("portfolio:contact"), {**self.data, "website": "spam.example"})
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_invalid_shows_errors(self):
        response = self.client.post(reverse("portfolio:contact"), {**self.data, "email": "bad"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_type_preselected_from_link(self):
        response = self.client.get(reverse("portfolio:contact"), {"type": "supplier"})
        self.assertContains(response, '<option value="supplier" selected>')


@override_settings(MEDIA_ROOT=TEST_MEDIA)
class AdminTests(TestCase):
    def test_admin_pages_load(self):
        call_command("seed_portfolio", stdout=StringIO())
        user = get_user_model().objects.create_superuser("admin", "a@example.com", "pw")
        self.client.force_login(user)
        for model in ("profile", "skill", "experience", "education", "project", "contactmessage"):
            with self.subTest(model=model):
                response = self.client.get(reverse(f"admin:portfolio_{model}_changelist"), follow=True)
                self.assertEqual(response.status_code, 200)

    def test_experience_dates_validated(self):
        bad = Experience(job_title="x", company="y", start_date=dt.date(2024, 5, 1), end_date=dt.date(2024, 1, 1))
        with self.assertRaises(Exception):
            bad.full_clean()
