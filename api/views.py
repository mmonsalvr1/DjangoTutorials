from rest_framework import generics
from pages.models import Product  
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
