from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save




class User(AbstractUser):
    Option=(
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    '''
        Users
    '''
    gender= models.CharField(max_length=50, choices=Option, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password', 'gender']

