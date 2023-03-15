import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    tier = models.ForeignKey('AccountTier', null=True, on_delete=models.SET_NULL)


class ThumbnailSize(models.Model):
    thumbnail_size = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.thumbnail_size)


class AccountTier(models.Model):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    ENTERPRISE = 'Enterprise'
    name = models.CharField(max_length=30, unique=True)
    thumbnail_size = models.ManyToManyField(ThumbnailSize, related_name="thumbnail_sizes", blank=True)
    fetch_expired = models.BooleanField(default=False)
    original_img = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    is_original = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)


class ExpiringLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='temps')
    created_at = models.DateTimeField(auto_now_add=True)
    expire_time = models.PositiveIntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)])

    def is_expired(self):
        expire_date = self.created_at + datetime.timedelta(seconds=self.expire_time)
        now = timezone.now()
        return expire_date < now
