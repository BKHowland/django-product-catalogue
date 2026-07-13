from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        fields = "__all__"
        
class ProductSearchQuerySerializer(serializers.Serializer):
    search = serializers.CharField(max_length=255, required=False)
    category = serializers.IntegerField(min_value=0, required=False)
    tags = serializers.ListField(child = serializers.IntegerField(min_value=0), required=False)
    
