from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User


# Create your models here.
# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(TimeStampMixin):
    ORDER_CHOICES = [
        ('a', 'Product A'),
        ('b', 'Product B'),
        ('c', 'Product C'),
    ]

    type = models.CharField(max_length=2, choices=ORDER_CHOICES)
    quantity = models.IntegerField(
        validators=[
            MaxValueValidator(200),
            MinValueValidator(1)
        ]
     )
    user = models.ForeignKey(User, related_name='user_order', on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('type', 'user')

    def __str__(self):
        return self.user.username + " " + str(self.id)


class Bid(TimeStampMixin):
    price = models.IntegerField(
        validators=[
            MaxValueValidator(10000000),
            MinValueValidator(1)
        ]
     )
    order = models.ForeignKey(Order, related_name='order_bid', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_bid', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('order', 'user')
        ordering = ['price']

    def __str__(self):
        return self.user.username + " " + str(self.id)


class Config(TimeStampMixin):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return 'Config: ' + self.name
