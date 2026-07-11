from rest_framework import serializers
from .models import Product

class ProductSearchQuerySerializer(serializers.Serializer):
    # for validating search filter query params.
    search = serializers.CharField(required=False, allow_blank=True)
    category = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.ListField(child = serializers.IntegerField(), required=False)

class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        fields = "__all__"