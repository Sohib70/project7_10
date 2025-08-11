from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Gullar(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
