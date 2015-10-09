from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class CommonInfo(models.Model):
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Common Information"
        verbose_name_plural = "Common Information"
        abstract = True


class DTUser(CommonInfo):
    USER_CHOICES = (
        ('R', 'Requester'),
        ('A', 'Approver'),
    )
    LOCATION_CHOICES = (
        ('L', 'Lake Success, New York'),
        ('S', 'Sacramento, California'),
        ('D', 'Dallas, Texas'),
        ('A', 'Alpharetta, Georgia'),
        ('SJ', 'South Jordan, Utah'),
        ('F', 'Field'),
    )
    user = models.OneToOneField(User)
    user_type = models.CharField(choices=USER_CHOICES, default='R', max_length=50)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=50)

    class Meta:
        verbose_name = "DT User"
        verbose_name_plural = "DT Users"

    def __unicode__(self):
        return self.user.username


class Inventory(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    description = models.CharField(blank=True, max_length=500)
    price = models.FloatField(default=0)
    picture = models.ImageField(upload_to='gadgetapp/static/gadgetapp/images/inventory_images/', null=True, blank=True)

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
    user = models.ForeignKey(DTUser, related_name='requester')
    approver = models.ForeignKey(DTUser, related_name='approver', null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now_add=False)
    status = models.CharField(choices=STATUS_CHOICES, default='R', max_length=50)
    notes = models.CharField(blank=True, max_length=500)
    approver_notes = models.CharField(blank=True, max_length=500)
    total_price = models.FloatField(blank = True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __unicode__(self):
        return self.id


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='orders')
    inventory = models.ForeignKey(Inventory)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def __unicode__(self):
        return self.id
