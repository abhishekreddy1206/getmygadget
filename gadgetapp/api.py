from rest_framework.views import APIView
from rest_framework.response import Response
from models import Inventory
from serializers import InventorySerializer


class InventoryList(APIView):
    def get(self):
        parent = Inventory.objects.all()
        inventory = parent.get_descendants(include_self=True)
        serialized_inventory_detail = InventorySerializer(inventory, many=True)
        return Response(serialized_inventory_detail.data)
