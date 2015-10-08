from rest_framework import serializers

from models import *


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'parent', 'level', 'price', 'description', 'picture')
