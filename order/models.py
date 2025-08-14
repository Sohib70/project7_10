from django.db import models
from pageapp.models import Gullar
from auth_user_.models import CustomUser
# Create your models here.


class Order(models.Model):
    STATUS_CHOISE = [
        ('pending','Pending'),
        ('paid','paid'),
        ("shipped","shipped"),
        ("canceled",'canceled')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOISE,default='pending')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

    @property
    def total_price(self):
        return sum(self.item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,blank=True,null=True,related_name='items')
    product = models.ForeignKey(Gullar,on_delete=models.CASCADE )
    amount = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.product.name

    @property
    def total_preice(self):
        return self.product.price * self.amount
