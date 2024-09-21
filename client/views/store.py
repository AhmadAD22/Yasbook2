from ..serializers.store import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from provider_details.models import Store,Reviews
from django.utils.translation import gettext_lazy as _

class StoreDetailView(APIView):
    def get(self, request, pk):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({"error": _("Store does not found!")},status=status.HTTP_404_NOT_FOUND)

        serializer = StoreADetailSerializer(store,context={'request': request})
        
        return Response(serializer.data,status=status.HTTP_200_OK)

