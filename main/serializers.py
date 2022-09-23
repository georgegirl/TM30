from .models import Product, Category, Cart
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    category= serializers.ReadOnlyField()

    class Meta:
        model= Product
        fields= '__all__'

class CategorySerializer(serializers.ModelSerializer):
    category_list= serializers.ReadOnlyField()
    
    class Meta:
        model= Category
        fields= ['category', 'desc', 'category_list']

class CartSerializer(serializers.ModelSerializer):
    cart= serializers.ReadOnlyField()

    class Meta:
        model= Cart
        fields= '__all__'


class CRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['Items', 'quantity']

class UserProductSerializer(serializers.ModelSerializer):
    orders_count = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['item', 'price', 'Stock', 'orders_count']