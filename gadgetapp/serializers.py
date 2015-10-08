from models import *
from rest_framework import serializers


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('id', 'name', 'parent', 'level', 'price', 'description', 'picture')