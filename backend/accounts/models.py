from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True,verbose_name="Email")
    display_name = models.CharField(max_length=100,blank=True,verbose_name="Display Name")
    bio = models.TextField(blank=True,null=True,verbose_name="Biography")
    avatar = models.ImageField(upload_to="avatars/",blank=True,null=True,verbose_name="Profile Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.display_name or self.username

