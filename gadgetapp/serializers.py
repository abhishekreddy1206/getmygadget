from rest_framework import serializers

from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'parent', 'level', 'price', 'description', 'picture')


class DTUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DTUser


class OrderDetailSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = OrderDetail


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderDetailSerializer(many=True, read_only=True)
    user = DTUserSerializer()

    class Meta:
        model = Order
