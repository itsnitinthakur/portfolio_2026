# portfolio/views.py
import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import ContactForm
from .models import ContactMessage, Education, Experience, Project, Skill

logger = logging.getLogger(__name__)

PUBLISHED_PROJECTS = Project.objects.published()


class HomeView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiences = Experience.objects.published().prefetch_related("skills")
        context.update(
            featured_projects=Project.objects.featured().prefetch_related("skills")[:6],
            featured_skills=Skill.objects.featured(),
            recent_experiences=experiences[:3],
            experience_count=experiences.count(),
            project_count=PUBLISHED_PROJECTS.count(),
        )
        return context


class ExperienceListView(ListView):
    template_name = "portfolio/experience_list.html"
    context_object_name = "experiences"

    def get_queryset(self):
        return Experience.objects.published().prefetch_related(
            "skills",
            Prefetch("projects", queryset=PUBLISHED_PROJECTS, to_attr="published_projects"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["education"] = Education.objects.published()
        return context


class ProjectListView(ListView):
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        queryset = PUBLISHED_PROJECTS.prefetch_related("skills").select_related("experience")
        self.active_skill = None
        skill_slug = self.request.GET.get("skill")
        if skill_slug:
            self.active_skill = get_object_or_404(Skill, slug=skill_slug)
            queryset = queryset.filter(skills=self.active_skill)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_skill"] = self.active_skill
        context["filter_skills"] = (
            Skill.objects.annotate(
                published_count=Count("projects", filter=Q(projects__is_published=True))
            )
            .filter(published_count__gt=0)
            .order_by("name")
        )
        return context


class ProjectDetailView(DetailView):
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return PUBLISHED_PROJECTS.select_related("experience").prefetch_related("skills")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["more_projects"] = (
            PUBLISHED_PROJECTS.exclude(pk=self.object.pk).prefetch_related("skills")[:3]
        )
        return context


class SkillListView(TemplateView):
    template_name = "portfolio/skill_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skills = Skill.objects.annotate(
            published_count=Count("projects", filter=Q(projects__is_published=True))
        )
        labels = dict(Skill.Category.choices)
        groups = {}
        for skill in skills:
            groups.setdefault(skill.category, []).append(skill)
        # Keep the category order defined on the model.
        context["skill_groups"] = [
            (labels[key], groups[key]) for key in labels if key in groups
        ]
        return context


class ContactView(FormView):
    template_name = "portfolio/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("portfolio:contact")

    def get_initial(self):
        initial = super().get_initial()
        inquiry = self.request.GET.get("type")
        if inquiry in ContactMessage.InquiryType.values:
            initial["inquiry_type"] = inquiry
        return initial

    def form_valid(self, form):
        if form.is_spam():
            # Pretend it worked so bots learn nothing.
            messages.success(self.request, "Thanks, your message has been sent.")
            return super().form_valid(form)

        contact = form.save()
        self.notify_owner(contact)
        messages.success(
            self.request,
            f"Thanks {contact.name}, your message has been sent. I'll reply to {contact.email}.",
        )
        return super().form_valid(form)

    def notify_owner(self, contact):
        recipient = settings.CONTACT_NOTIFY_EMAIL
        if not recipient:
            return
        body = (
            f"From: {contact.name} <{contact.email}>\n"
            f"Company: {contact.company or '-'}\n"
            f"Country: {contact.country or '-'}\n"
            f"Phone / WhatsApp: {contact.phone or '-'}\n"
            f"WeChat: {contact.wechat_id or '-'}\n"
            f"Type: {contact.get_inquiry_type_display()}\n\n"
            f"{contact.message}\n"
        )
        try:
            send_mail(
                subject=f"[Portfolio] {contact.subject}",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
            )
        except Exception:  # The message is already saved; email is a bonus.
            logger.exception("Could not send contact notification email")
