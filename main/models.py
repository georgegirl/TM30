from unicodedata import category
from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import User
from django.forms import model_to_dict


# Create your models here.
class Category(models.Model):
    category= models.CharField(max_length=300,unique=True)
    desc= models.TextField(max_length=255, null=True)
    date_added= models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.category

class Product(models.Model):
    CHOICE_STAT=(
        ('available', 'available'),
        ('unavailable', 'unavailable')
    )
    
    name= models.ForeignKey(Category, related_name= "Product",on_delete= models.CASCADE)
    item= models.CharField(max_length=300)
    slug= models.SlugField(max_length=300, blank=True, null=True)
    
    Stock = models.FloatField(default=0)
    price= models.FloatField() 
    status= models.CharField(max_length=50,choices=CHOICE_STAT)
    date_added= models.DateTimeField(auto_now_add=True) 
    

    class Meta:
        ordering = ('name',)


    def __str__(self):
        return self.name

    @property
    def category(self):
        return model_to_dict(self.name, fields= ['category'])

    @property
    def orders_count(self):
        return self.name.all().values().count()

class Cart(models.Model):
    owner= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='now')
    Items= models.ForeignKey(Product, blank=True,on_delete=models.CASCADE, related_name='Items')
    quantity= models.IntegerField(default=1)
    Done_shopping = models.BooleanField(default=False)
    date_added= models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{User.objects.get(username=self.owner)}'s cart"
    
    @property
    def cart_content(self):
        return model_to_dict(self.cart_item, fields=['Item', 'price'])
    

