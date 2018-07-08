from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = False)
    thumb = models.ImageField(default = 'default.jpg', blank = True)
    owner = models.ForeignKey(User, default = None, on_delete = 'CASCADE')

    def __str__(self):
        return self.name
