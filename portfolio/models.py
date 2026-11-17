# portfolio/models.py
"""
Database models for the portfolio app.

Profile         the site owner: name, bio, photo and contact links (one row)
Company         the company the owner represents, for customers and suppliers (one row)
Product         a machine or product line the company supplies
Skill          a technology or capability, grouped by category
Experience      a role on the career timeline
Education       a qualification
Project         something built, linked to its skills and (optionally) a role
ContactMessage  an enquiry submitted through the public contact form
"""

from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils.text import slugify


def build_unique_slug(instance, value, max_length=50):
    """Return a slug for ``value`` that no other row of the same model uses."""
    base = slugify(value)[:max_length] or "item"
    slug = base
    counter = 2
    queryset = type(instance).objects.exclude(pk=instance.pk)
    while queryset.filter(slug=slug).exists():
        suffix = f"-{counter}"
        slug = f"{base[: max_length - len(suffix)]}{suffix}"
        counter += 1
    return slug


class TimeStampedModel(models.Model):
    """Abstract base that records when a row was created and last changed."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #
class Profile(TimeStampedModel):
    """The site owner. The table holds a single row, edited in the admin."""

    full_name = models.CharField(max_length=120)
    headline = models.CharField(
        max_length=160,
        help_text="One line shown under your name.",
    )
    bio = models.TextField(
        help_text="About-me text. Separate paragraphs with a blank line.",
    )
    open_to = models.CharField(
        max_length=200,
        blank=True,
        help_text="What you want to hear about, for example: Supplier partnerships and automation projects.",
    )
    photo = models.ImageField(upload_to="profile/", blank=True)
    photo_alt = models.CharField(
        max_length=160,
        blank=True,
        help_text="Describes the photo for screen readers.",
    )
    location = models.CharField(max_length=120, blank=True)
    company = models.CharField(
        max_length=120,
        blank=True,
        help_text="The company you represent.",
    )
    company_url = models.URLField("Company URL", blank=True)
    email = models.EmailField(
        blank=True,
        help_text="Public contact address shown on the site.",
    )
    phone = models.CharField("Phone / WhatsApp", max_length=40, blank=True)
    wechat_id = models.CharField("WeChat ID", max_length=60, blank=True)
    github_url = models.URLField("GitHub URL", blank=True)
    linkedin_url = models.URLField("LinkedIn URL", blank=True)
    resume = models.FileField(
        upload_to="profile/",
        blank=True,
        help_text="Optional PDF offered as a download.",
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1  # single-row table: every save writes the same row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the profile row, or None if it has not been created yet."""
        return cls.objects.filter(pk=1).first()


# --------------------------------------------------------------------------- #
# Company and its products
# --------------------------------------------------------------------------- #
class Company(TimeStampedModel):
    """The company the site owner represents. The table holds a single row."""

    name = models.CharField(max_length=160)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(
        help_text="Separate paragraphs with a blank line.",
    )
    website = models.URLField(blank=True)
    established_year = models.PositiveSmallIntegerField(null=True, blank=True)
    staff_count = models.PositiveIntegerField(null=True, blank=True)
    engineer_count = models.PositiveIntegerField(null=True, blank=True)
    unit_count = models.PositiveSmallIntegerField(
        "manufacturing units", null=True, blank=True
    )
    certifications = models.CharField(
        max_length=200,
        blank=True,
        help_text="Only list certificates that are current.",
    )
    capabilities = models.TextField(
        blank=True,
        help_text="One per line, for example: Installation and after-sales service.",
    )
    clients = models.TextField(
        blank=True,
        help_text="One client name per line. Shown as 'Clients include'.",
    )
    offices = models.TextField(
        blank=True,
        help_text="One office per line, for example: Corporate office: A-6, ..., New Delhi 110015",
    )
    sales_email = models.EmailField(blank=True)
    sales_phone = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "company"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1  # single-row table
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.filter(pk=1).first()

    @staticmethod
    def _lines(text):
        return [line.strip() for line in text.splitlines() if line.strip()]

    @property
    def capability_list(self):
        return self._lines(self.capabilities)

    @property
    def client_list(self):
        return self._lines(self.clients)

    @property
    def office_list(self):
        return self._lines(self.offices)


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def featured(self):
        return self.published().filter(is_featured=True)


class Product(TimeStampedModel):
    class Category(models.TextChoices):
        WELDING = "welding", "Ultrasonic welding"
        CUTTING = "cutting", "Ultrasonic cutting & sewing"
        BAG_MAKING = "bag_making", "Bag making"
        PRINTING = "printing", "Printing"
        INDUCTION = "induction", "Induction heating"
        CLEANING = "cleaning", "Cleaning, drilling & other"
        COMPONENTS = "components", "Ultrasonic components"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    summary = models.CharField(max_length=240, blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    image_alt = models.CharField(max_length=160, blank=True)
    url = models.URLField("More details URL", blank=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured products appear on the home page.",
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["category", "order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["company", "name"], name="product_unique_per_company"),
        ]

    def __str__(self):
        return self.name


# --------------------------------------------------------------------------- #
# Skill
# --------------------------------------------------------------------------- #
class SkillQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(is_featured=True)


class Skill(TimeStampedModel):
    class Category(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DEVOPS = "devops", "DevOps & Cloud"
        DATABASE = "database", "Databases"
        ERP = "erp", "ERP & Business Systems"
        VISION = "vision", "Computer Vision & Automation"
        TOOLS = "tools", "Tools & Workflow"
        OTHER = "other", "Other"

    class Level(models.IntegerChoices):
        FAMILIAR = 1, "Familiar"
        PROFICIENT = 2, "Proficient"
        ADVANCED = 3, "Advanced"
        EXPERT = 4, "Expert"

    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.BACKEND,
        db_index=True,
    )
    level = models.PositiveSmallIntegerField(
        choices=Level.choices,
        null=True,
        blank=True,
        help_text="Optional. Leave empty to list the skill without a level bar.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured skills appear on the home page.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers are shown first within a category.",
    )

    objects = SkillQuerySet.as_manager()

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_unique_slug(self, self.name, max_length=70)
        super().save(*args, **kwargs)

    @property
    def level_percent(self):
        """Level as 25 / 50 / 75 / 100 for a progress bar, or None if no level is set."""
        return self.level * 25 if self.level else None


# --------------------------------------------------------------------------- #
# Experience
# --------------------------------------------------------------------------- #
class ExperienceQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def current(self):
        return self.published().filter(end_date__isnull=True)


class Experience(TimeStampedModel):
    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship / Co-op"
        FREELANCE = "freelance", "Freelance"

    job_title = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    company_url = models.URLField(blank=True)
    location = models.CharField(
        max_length=120,
        blank=True,
        help_text="For example: New Delhi, India",
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
    )
    start_date = models.DateField()
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave empty if this is your current role.",
    )
    summary = models.TextField(
        blank=True,
        help_text="Two or three sentences on what the role covered.",
    )
    highlights = models.TextField(
        blank=True,
        help_text="One achievement per line. Each line becomes a bullet point.",
    )
    skills = models.ManyToManyField(Skill, related_name="experiences", blank=True)
    is_published = models.BooleanField(default=True)

    objects = ExperienceQuerySet.as_manager()

    class Meta:
        # Current roles (no end date) first, then the most recent.
        ordering = [F("end_date").desc(nulls_first=True), "-start_date"]
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__isnull=True) | Q(end_date__gte=F("start_date")),
                name="experience_end_not_before_start",
                violation_error_message="End date cannot be before the start date.",
            ),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company}"

    @property
    def is_current(self):
        return self.end_date is None

    @property
    def highlight_list(self):
        """Highlights as a list of non-empty lines, ready to loop over."""
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]


# --------------------------------------------------------------------------- #
# Education
# --------------------------------------------------------------------------- #
class EducationQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class Education(TimeStampedModel):
    institution = models.CharField(max_length=160)
    qualification = models.CharField(
        max_length=160,
        help_text="For example: Bachelor of Computer Applications.",
    )
    field_of_study = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_year = models.PositiveSmallIntegerField(null=True, blank=True)
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    honours = models.CharField(
        max_length=120,
        blank=True,
        help_text="For example: Dean's Honours.",
    )
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers are shown first.",
    )
    is_published = models.BooleanField(default=True)

    objects = EducationQuerySet.as_manager()

    class Meta:
        ordering = ["order", F("end_year").desc(nulls_last=True)]
        verbose_name = "education entry"
        verbose_name_plural = "education"
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(start_year__isnull=True)
                    | Q(end_year__isnull=True)
                    | Q(end_year__gte=F("start_year"))
                ),
                name="education_end_not_before_start",
                violation_error_message="End year cannot be before the start year.",
            ),
        ]

    def __str__(self):
        return f"{self.qualification}, {self.institution}"


# --------------------------------------------------------------------------- #
# Project
# --------------------------------------------------------------------------- #
class ProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def featured(self):
        return self.published().filter(is_featured=True)


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        COMPLETED = "completed", "Completed"
        IN_PROGRESS = "in_progress", "In progress"
        LIVE = "live", "Live & maintained"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(
        max_length=220,
        help_text="One or two lines shown on project cards.",
    )
    description = models.TextField(
        help_text="Full write-up for the detail page: the problem, what you built, the result.",
    )
    impact = models.CharField(
        max_length=220,
        blank=True,
        help_text="Headline result, for example: Cut manual counting time by 80%.",
    )
    role = models.CharField(
        max_length=120,
        blank=True,
        help_text="Your part in the project, for example: Sole developer.",
    )
    experience = models.ForeignKey(
        Experience,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
        help_text="The job this was built in, if any.",
    )
    skills = models.ManyToManyField(Skill, related_name="projects", blank=True)
    cover_image = models.ImageField(upload_to="projects/covers/", blank=True)
    cover_image_alt = models.CharField(
        max_length=160,
        blank=True,
        help_text="Describes the image for screen readers.",
    )
    github_url = models.URLField("GitHub URL", blank=True)
    live_url = models.URLField("Live URL", blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured projects appear on the home page.",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Untick to hide this project from the public site.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers are shown first.",
    )

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ["order", "-created_at"]
        indexes = [
            models.Index(
                fields=["is_published", "is_featured"],
                name="project_pub_feat_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(start_date__isnull=True)
                    | Q(end_date__isnull=True)
                    | Q(end_date__gte=F("start_date"))
                ),
                name="project_end_not_before_start",
                violation_error_message="End date cannot be before the start date.",
            ),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_unique_slug(self, self.title, max_length=140)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})


# --------------------------------------------------------------------------- #
# ContactMessage
# --------------------------------------------------------------------------- #
class ContactMessageQuerySet(models.QuerySet):
    def unread(self):
        return self.filter(status=ContactMessage.Status.NEW)


class ContactMessage(models.Model):
    class InquiryType(models.TextChoices):
        MACHINE = "machine", "Buying a machine / price quote"
        CLIENT = "client", "Client / customer project"
        SUPPLIER = "supplier", "Supplier / manufacturer"
        PARTNERSHIP = "partnership", "Sales / partnership"
        HIRING = "hiring", "Job opportunity"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        NEW = "new", "New"
        READ = "read", "Read"
        REPLIED = "replied", "Replied"
        SPAM = "spam", "Spam"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160, blank=True)
    country = models.CharField(max_length=80, blank=True)
    phone = models.CharField("Phone / WhatsApp", max_length=40, blank=True)
    wechat_id = models.CharField("WeChat ID", max_length=60, blank=True)
    inquiry_type = models.CharField(
        max_length=20,
        choices=InquiryType.choices,
        default=InquiryType.CLIENT,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries",
        verbose_name="product of interest",
    )
    subject = models.CharField(max_length=160)
    message = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Private notes. Never shown on the public site.",
    )
    created_at = models.DateTimeField("received", auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    objects = ContactMessageQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status", "-created_at"],
                name="contact_status_created_idx",
            ),
        ]
        verbose_name = "contact message"
        verbose_name_plural = "contact messages"

    def __str__(self):
        return f"{self.name}: {self.subject}"
