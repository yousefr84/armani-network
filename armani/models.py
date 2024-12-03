from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(blank=True, null=True,max_length=11)
    Photo = models.ImageField(upload_to='image/', blank=True, default='Site/Mamozio.png')
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    is_mentor = models.BooleanField(default=True)


class Services(models.Model):
    services = {
        "MT": 'مشاوره فروش و مارکتینگ',
        "IM": 'سرمایه گذاری',
        "FB": 'تدوین طرح توجیهی و طرح کسب و کار',
        "FA": 'خدمات مالی و حسابداری',
        "LG": 'خدمات حقوقی',
    }

    name = models.CharField(max_length=2, choices=services)
    id = models.AutoField(primary_key=True)


class Clients(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    looking_for = models.ManyToManyField(Services)


class Mentor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Mentor_profile')
    job_position = models.CharField(max_length=100)
    services = models.ManyToManyField(Services, blank=True)
    banner = models.ImageField(upload_to='image/', blank=True)


class Articles(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='article_profile')
    made_date = models.DateField(auto_now_add=True)
    body = models.TextField()
