from models import *
from serializers import *
from django.http import Http404
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

class InventoryList(APIView):
    def get(self, request, format=None):
        parent = Inventory.objects.all()
        inventory = parent.get_descendants(include_self=True)
        serialized_inventory_detail = InventorySerializer(inventory, many=True)
        return Response(serialized_inventory_detail.data)