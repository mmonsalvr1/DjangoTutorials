from rest_framework import serializers
from pages.models import (Product)  # ajusta si tu modelo está en pages.models o donde sea


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
