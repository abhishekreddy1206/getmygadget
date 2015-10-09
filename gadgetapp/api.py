from rest_framework.views import APIView
from rest_framework.response import Response

from models import Inventory, Order
from serializers import InventorySerializer, OrderSerializer


class InventoryList(APIView):
    def get(self, request, format=None):
        parent = Inventory.objects.all()
        inventory = parent.get_descendants(include_self=True)
        serialized_inventory_detail = InventorySerializer(inventory, many=True)
        return Response(serialized_inventory_detail.data)

class GetLatestOrderUser(APIView):
    def get(self, request, format=None):
        order = [Order.objects.filter(user__user = request.user).order_by('-id')[0]]
        serialized_order = OrderSerializer(order, many=True)
        return Response(serialized_order.data)

class UserOrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(user__user = request.user).order_by('id')
        serialized_orders = OrderSerializer(orders, many=True)
        return Response(serialized_orders.data)