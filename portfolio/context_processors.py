# portfolio/context_processors.py
from .models import Company, Profile


def site_profile(request):
    """Make the owner's profile and company available to every template."""
    return {"profile": Profile.load(), "company": Company.load()}
