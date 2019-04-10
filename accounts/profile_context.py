from .models import Profile,Post
from django.core.exceptions import ObjectDoesNotExist


def context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            post=Post.objects.filter(user=request.user)
            if post.exists():
                post=post.first()
            else:
                post=0
            return {'profile': profile,'post':post}
        except ObjectDoesNotExist:
            return {'profile': 0,'post':0}

    else:
        return {'profile': 0,'post':0}