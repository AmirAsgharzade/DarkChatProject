from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
import random
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        colors = [
    "#00BFFF",  # Electric Blue
    "#00FFFF",  # Soft Cyan
    "#00FF00",  # Bright Green
    "#32CD32",  # Lime Green
    "#FFFF00",  # Neon Yellow
    "#FF7F50",  # Coral
    "#FF69B4",  # Hot Pink
    "#FF00FF",  # Magenta
    "#F08080",  # Light Coral
    "#87CEEB",  # Sky Blue
    "#DAA520",  # Goldenrod
    "#FFA07A",  # Light Salmon
    "#BA55D3",  # Medium Orchid
    "#40E0D0",  # Turquoise
    "#EE82EE",  # Violet
    "#FA8072",  # Salmon
    "#20B2AA",  # Light Sea Green
    "#3CB371",  # Medium Sea Green
    "#DA70D6",  # Orchid
    "#00BFFF",  # Deep Sky Blue
    "#FF6347",  # Tomato
    "#6A5ACD",  # Slate Blue
    "#2E8B57",  # Sea Green
    "#DC143C",  # Crimson
    "#FAFAD2",  # Light Goldenrod Yellow
    "#DB7093",  # Pale Violet Red
    "#48D1CC",  # Medium Turquoise
    "#FF8C00",  # Dark Orange
    "#4682B4",  # Steel Blue
    "#4B0082",  # Indigo
    "#FFDAB9",  # Peach Puff
    "#778899",  # Light Slate Gray
    "#9932CC",  # Dark Orchid
    "#00FF7F",  # Spring Green
    "#ADD8E6",  # Light Blue
    "#CCCCFF",  # Periwinkle
    "#E6E6FA",  # Lavender
    "#7FFF00",  # Chartreuse
    "#B22222",  # Firebrick
    "#4169E1"   # Royal Blue
    ]   
        if not username:
            raise ValueError('The usename Field must be set')
        elif not password:
            raise ValueError('Password Field must be set')
        
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.set_color(random.choice(colors))
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        return self.create_user(username,password,**extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    
    username= models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    color = models.CharField(max_length=16)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username
    
    def set_color(self,color):
        self.color = color

    