from django.db import models
from conf.settings import AUTH_USER_MODEL
from pageapp.models import Gullar

User = AUTH_USER_MODEL

class Card(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items)

class CardItem(models.Model):
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    gul = models.ForeignKey(Gullar,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.gul.name

    @property
    def total_price(self):
        return self.gul.price * self.amount
