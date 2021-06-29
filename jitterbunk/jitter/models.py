from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True, primary_key=True)
    photo = models.CharField(max_length=200, default='https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png')
    date_joined = models.DateTimeField(auto_now_add=True)
    num_bunks = models.IntegerField(default=0)
    logged_in = models.BooleanField(default=False)  

    def __str__(self):
        return self.username

class Bunk(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "bunk from: " + self.from_user.username + " to: " + self.to_user.username
