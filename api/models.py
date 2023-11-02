from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    staff = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staf')

    def __str__(self) -> str:
        return self.user.username

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pic')
    img = models.ImageField(upload_to='images')

class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dt = models.DateTimeField(auto_created=True, auto_now=True)