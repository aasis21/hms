from .models import Billers
from django.core.exceptions import ObjectDoesNotExist


def context(request):
    if request.user.is_authenticated:
        try:
            biller = Billers.objects.get(user=request.user)
            return {'biller': biller}
        except ObjectDoesNotExist:
            return {'biller': 0}

    else:
        return {'biller': 0}