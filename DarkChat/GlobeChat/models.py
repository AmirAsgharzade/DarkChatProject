from django.db import models
from Authen.models import CustomUser
# Create your models here.


class GlobeHistory(models.Model):
    user= models.ForeignKey(CustomUser,to_field='username',on_delete=models.CASCADE,related_name='message')
    username = models.CharField(max_length=255,null=True,blank=True)
    color = models.CharField(max_length=16,null=True,blank=True)
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if self.user:
            username = self.user.username
            color = self.user.color
        super().save(*args,**kwargs)


