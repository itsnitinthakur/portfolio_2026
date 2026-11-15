# portfolio/context_processors.py
from .models import Profile


def site_profile(request):
    """Make the site owner's profile available to every template as `profile`."""
    return {"profile": Profile.load()}
