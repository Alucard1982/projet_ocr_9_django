from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from litLogin.models import User
from django_userforeignkey.models.fields import UserForeignKey


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    time_created = models.DateTimeField(auto_now=True)
    boolean = models.BooleanField(default=False)
    user = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)


class Review(models.Model):
    headline = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)


class UserFollows(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)


