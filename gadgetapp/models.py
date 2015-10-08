from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
import datetime

# Create your models here.

class DTUser(models.Model):
    USER_CHOICES = (
        ('R', 'Requester'),
        ('A', 'Approver'),
    )
    user = models.OneToOneField(User)
    user_type = models.CharField(choices=USER_CHOICES, default='R', max_length=50)

    class Meta:
        verbose_name = "DT User"
        verbose_name_plural = "DT Users"

    def __unicode__(self):
        return self.user.username

class Inventory(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    description = models.CharField(blank=True, max_length=500)
    price = models.FloatField(default = 0)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __unicode__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('R', 'Received'),
        ('A', 'Approved'),
        ('RE', 'Rejected'),
        ('D', 'Dispatched')
    )
    user = models.ForeignKey(User, related_name='requester')
    approver = models.ForeignKey(User, related_name='approver', blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='R', max_length=50)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __unicode__(self):
        return self.id

class OrderDetail(models.Model):
    order = models.ForeignKey(Order)
    inventory = models.ForeignKey(Inventory)
    quantity = models.IntegerField(default = 1)

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def __unicode__(self):
        return self.id
