from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from models import *


# Register your models here.


class InventoryAdmin(DjangoMpttAdmin):
    pass


admin.site.register(DTUser)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Order)
admin.site.register(OrderDetail)
