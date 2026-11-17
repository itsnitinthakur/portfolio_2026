# portfolio/urls.py
from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("experience/", views.ExperienceListView.as_view(), name="experience"),
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("skills/", views.SkillListView.as_view(), name="skills"),
    path("machines/", views.CompanyView.as_view(), name="company"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
