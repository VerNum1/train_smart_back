from rest_framework import serializers
from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'price',
            'image_url',
            'store_links',
            'sport_types',
            'target_gender'
        ]