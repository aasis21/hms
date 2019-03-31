from .models import Profile
from django.core.exceptions import ObjectDoesNotExist


def context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'profile': profile}
        except ObjectDoesNotExist:
            return {'profile': 0}

    else:
        return {'profile': 0}