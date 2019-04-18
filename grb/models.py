from django.db import models
from django.contrib.auth.models import User
# from hms.settings import GR_COUNT
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS_CHOICES = (
    ('B', 'Booked'),
    ('P', 'Pending'),
    ('C', 'Cancelled')
    )
    booking_status = models.CharField(choices = STATUS_CHOICES, max_length=1, default = 'P')
    room = models.IntegerField()
