from django.db import models
from django.contrib.auth.models import User 

class UserProfile(models.Model):
    user = models.OneToOneField(User,default=None,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/',default="images/avatar-default.jpg")
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.user.email
    


