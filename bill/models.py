from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Billers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    def __str__(self):
        return self.name
    
class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill=models.IntegerField()
    biller=models.ForeignKey(Billers, on_delete=models.CASCADE)
    reason=models.CharField(max_length=150)
    time=models.DateTimeField(auto_now_add=True)
    @property
    def nbill(self):
        return -1*self.bill
    def __str__(self):
        return self.user.username+"[ "+self.biller.name+" ] = "+str(self.bill) +"      ( "+str(self.time)+" )"

class Messrem(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    start=models.DateField()
    end=models.DateField()
    status=models.IntegerField(default=0)
    @property
    def link(self):
        return '/bills/rmremb/'+str(self.id)