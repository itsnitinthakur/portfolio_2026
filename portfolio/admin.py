# portfolio/admin.py
"""Admin configuration for the portfolio app."""

from urllib.parse import quote

from django.contrib import admin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    Company,
    ContactMessage,
    Education,
    Experience,
    Product,
    Profile,
    Project,
    Skill,
)

admin.site.site_header = "Portfolio administration"
admin.site.site_title = "Portfolio admin"
admin.site.index_title = "Manage site content"


# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """One row only: the list page goes straight to the edit form."""

    readonly_fields = ("photo_preview",)
    fieldsets = (
        (None, {"fields": ("full_name", "headline", "bio", "open_to")}),
        ("Photo", {"fields": ("photo", "photo_preview", "photo_alt")}),
        ("Where you work", {"fields": ("location", "company", "company_url")}),
        ("Contact & links", {"fields": ("email", "phone", "wechat_id", "github_url", "linkedin_url", "resume")}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        profile = Profile.load()
        if profile is not None:
            return redirect(reverse("admin:portfolio_profile_change", args=[profile.pk]))
        return super().changelist_view(request, extra_context)

    @admin.display(description="Preview")
    def photo_preview(self, obj):
        if not obj.photo:
            return "Upload a photo and save to see a preview."
        return format_html(
            '<img src="{}" alt="" style="width:160px;height:160px;object-fit:cover;border-radius:50%;">',
            obj.photo.url,
        )


# --------------------------------------------------------------------------- #
# Company and products
# --------------------------------------------------------------------------- #
class ProductInline(admin.TabularInline):
    model = Product
    fields = ("name", "category", "summary", "is_featured", "is_published", "order")
    extra = 0
    show_change_link = True


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """One row only: the list page goes straight to the edit form."""

    inlines = (ProductInline,)
    fieldsets = (
        (None, {"fields": ("name", "tagline", "description", "website")}),
        ("Key facts", {"fields": ("established_year", "staff_count", "engineer_count", "unit_count", "certifications")}),
        ("What you offer", {"fields": ("capabilities", "clients")}),
        ("Sales contact", {"fields": ("sales_email", "sales_phone", "offices")}),
    )

    def has_add_permission(self, request):
        return not Company.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        company = Company.load()
        if company is not None:
            return redirect(reverse("admin:portfolio_company_change", args=[company.pk]))
        return super().changelist_view(request, extra_context)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_featured", "is_published", "order", "enquiry_count")
    list_editable = ("is_featured", "is_published", "order")
    list_filter = ("category", "is_featured", "is_published")
    search_fields = ("name", "summary")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_enquiries=Count("enquiries"))

    @admin.display(description="Enquiries", ordering="_enquiries")
    def enquiry_count(self, obj):
        return obj._enquiries


# --------------------------------------------------------------------------- #
# Skill
# --------------------------------------------------------------------------- #
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "is_featured", "order", "project_count")
    list_editable = ("level", "is_featured", "order")
    list_filter = ("category", "level", "is_featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_project_count=Count("projects"))

    @admin.display(description="Projects", ordering="_project_count")
    def project_count(self, obj):
        return obj._project_count


# --------------------------------------------------------------------------- #
# Experience
# --------------------------------------------------------------------------- #
class ProjectInline(admin.TabularInline):
    """Read-only list of the projects linked to a role."""

    model = Project
    fields = ("title", "status", "is_published")
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True
    verbose_name_plural = "Projects built in this role"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "location",
        "employment_type",
        "start_date",
        "end_date",
        "current",
        "is_published",
    )
    list_editable = ("is_published",)
    list_filter = ("employment_type", "is_published")
    search_fields = ("job_title", "company", "location", "summary", "highlights")
    filter_horizontal = ("skills",)
    inlines = (ProjectInline,)
    fieldsets = (
        (None, {"fields": ("job_title", "company", "company_url", "location", "employment_type")}),
        ("Dates", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("summary", "highlights", "skills")}),
        ("Visibility", {"fields": ("is_published",)}),
    )

    @admin.display(boolean=True, description="Current")
    def current(self, obj):
        return obj.is_current


# --------------------------------------------------------------------------- #
# Education
# --------------------------------------------------------------------------- #
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("qualification", "institution", "honours", "start_year", "end_year", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("qualification", "institution", "field_of_study")


# --------------------------------------------------------------------------- #
# Project
# --------------------------------------------------------------------------- #
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "cover_thumbnail",
        "title",
        "status",
        "experience",
        "is_featured",
        "is_published",
        "order",
        "updated_at",
    )
    list_display_links = ("cover_thumbnail", "title")
    list_editable = ("is_featured", "is_published", "order")
    list_filter = (
        "status",
        "is_featured",
        "is_published",
        ("skills", admin.RelatedOnlyFieldListFilter),
    )
    list_select_related = ("experience",)
    search_fields = ("title", "summary", "description", "impact")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("skills",)
    readonly_fields = ("cover_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "description", "impact")}),
        ("Context", {"fields": ("role", "experience", "skills", "status", "start_date", "end_date")}),
        ("Media & links", {"fields": ("cover_image", "cover_preview", "cover_image_alt", "github_url", "live_url")}),
        ("Visibility", {"fields": ("is_published", "is_featured", "order")}),
        ("Record", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Cover")
    def cover_thumbnail(self, obj):
        if not obj.cover_image:
            return "No image"
        return format_html(
            '<img src="{}" alt="" style="width:64px;height:40px;object-fit:cover;border-radius:4px;">',
            obj.cover_image.url,
        )

    @admin.display(description="Preview")
    def cover_preview(self, obj):
        if not obj.cover_image:
            return "Upload an image and save to see a preview."
        return format_html(
            '<img src="{}" alt="" style="max-width:320px;height:auto;border-radius:6px;">',
            obj.cover_image.url,
        )


# --------------------------------------------------------------------------- #
# ContactMessage
# --------------------------------------------------------------------------- #
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Works as an inbox: messages arrive from the site and are triaged here."""

    list_display = ("name", "email", "company", "country", "inquiry_type", "product", "subject", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "inquiry_type", "product", "created_at")
    search_fields = ("name", "email", "company", "country", "subject", "message")
    date_hierarchy = "created_at"
    actions = ("mark_as_read", "mark_as_replied", "mark_as_spam")
    readonly_fields = (
        "name",
        "email",
        "company",
        "country",
        "phone",
        "wechat_id",
        "inquiry_type",
        "product",
        "subject",
        "message",
        "created_at",
        "replied_at",
        "reply_by_email",
    )
    fieldsets = (
        ("Sender", {"fields": ("name", "email", "company", "country", "phone", "wechat_id")}),
        ("Message", {"fields": ("inquiry_type", "product", "subject", "message", "created_at")}),
        ("Follow-up", {"fields": ("status", "reply_by_email", "replied_at", "admin_notes")}),
    )

    def has_add_permission(self, request):
        # Messages are only created through the public contact form.
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Opening a new message counts as reading it.
        if request.method == "GET" and str(object_id).isdigit() and self.has_change_permission(request):
            ContactMessage.objects.filter(
                pk=object_id, status=ContactMessage.Status.NEW
            ).update(status=ContactMessage.Status.READ)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if obj.status == ContactMessage.Status.REPLIED and obj.replied_at is None:
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)

    @admin.display(description="Reply")
    def reply_by_email(self, obj):
        return format_html(
            '<a class="button" href="mailto:{}?subject={}">Reply by email</a>',
            obj.email,
            quote(f"Re: {obj.subject}"),
        )

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.filter(status=ContactMessage.Status.NEW).update(
            status=ContactMessage.Status.READ
        )
        self.message_user(request, f"{updated} message(s) marked as read.")

    @admin.action(description="Mark selected messages as replied")
    def mark_as_replied(self, request, queryset):
        updated = queryset.exclude(status=ContactMessage.Status.REPLIED).update(
            status=ContactMessage.Status.REPLIED, replied_at=timezone.now()
        )
        self.message_user(request, f"{updated} message(s) marked as replied.")

    @admin.action(description="Mark selected messages as spam")
    def mark_as_spam(self, request, queryset):
        updated = queryset.update(status=ContactMessage.Status.SPAM)
        self.message_user(request, f"{updated} message(s) marked as spam.")
