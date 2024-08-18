from rest_framework import serializers
from .product import ProductSerializer
from ..models.action import CartItem, Cart, BannerAds, Product
from .user import UserSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'subtotal']
        read_only_fields = ['user', 'subtotal']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data.pop('product_id')
        cart_item = CartItem.objects.create(user=user, product=product, **validated_data)
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        if 'product_id' in validated_data:
            instance.product = validated_data['product_id']
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total']

    def get_total(self, obj):
        return obj.total()

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.create(user=user)
        return cart

    def update(self, instance, validated_data):
        return instance

class BannerAdsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = BannerAds
        fields = ['id', 'name', 'product', 'product_id']

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        banner_ad = BannerAds.objects.create(product=product, **validated_data)
        return banner_ad

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if 'product_id' in validated_data:
            instance.product = validated_data['product_id']
        instance.save()
        return instance