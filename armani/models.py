from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_mentor = models.BooleanField(default=False)


class Services(models.Model):
    services = {
        "MT": 'مشاوره فروش و مارکتینگ',
        "IM": 'سرمایه گذاری',
        "FB": 'تدوین طرح توجیهی و طرح کسب و کار',
        "FA": 'خدمات مالی و حسابداری',
        "LG": 'خدمات حقوقی',
    }

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2, choices=services)

class Mentors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    job_position = models.CharField(max_length=100)
    Services = models.ManyToManyField(Services)
    Photo = models.ImageField(upload_to='image/', blank=True, default='Site/Mamozio.png')
    banner = models.ImageField(upload_to='image/', blank=True)



