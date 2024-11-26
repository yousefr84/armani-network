from django.db import models

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
    Job_position = models.CharField(max_length=100)
    Services = models.ManyToManyField(Services)


