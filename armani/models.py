from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField
from django.utils import timezone


class Services(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

class Label(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(blank=True, null=True, max_length=11, unique=True)
    Photo = models.ImageField(upload_to='image/', blank=True,null=True,default='default_images/l60Hf.png')
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    identification_code = models.CharField(blank=True, null=True, max_length=10)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    looking_for = models.ManyToManyField(Services, blank=True)
    job_position = models.CharField(max_length=100, blank=True, null=True)
    services = models.ManyToManyField(Services, blank=True, related_name='mentors')
    banner = models.ImageField(upload_to='image/', blank=True, null=True)
    # project = models.ManyToManyField(Label, blank=True, related_name='mentors')
    city = models.CharField(max_length=100, blank=True, null=True)
    social_networks = JSONField(default=dict, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)





# class Clients(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
#     looking_for = models.ManyToManyField(Services)

#
# class Mentor(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Mentor_profile')
#     job_position = models.CharField(max_length=100)
#     services = models.ManyToManyField(Services, blank=True, related_name='mentors')
#     banner = models.ImageField(upload_to='image/', blank=True, null=True)
#     project = models.ManyToManyField(Label, blank=True, related_name='mentors')
#     city = models.CharField(max_length=100, blank=True, null=True)
#     social_networks = JSONField(default=dict, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)

class Articles(models.Model):
    name = models.CharField(max_length=100)
    made_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='article_profile')
    type = 'article'
    made_date = models.DateField(auto_now_add=True)
    public_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles_public')
    description = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='image/', blank=True)
    is_readed = models.BooleanField(default=False)



class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    labels = models.ManyToManyField(Label, blank=True, related_name='projects')
    members = models.ManyToManyField(CustomUser, related_name='projects_members', blank=True)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='project', blank=True, null=True)
    rate = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='image/', blank=True, default='Site/Mamozio.png')
    date_of_start = models.DateField(auto_now_add=True)
    date_of_end = models.DateField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
