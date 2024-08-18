from rest_framework import serializers
from ..models.order import Order, Transaction, CartItem
from user.serializers import UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_code', 'user', 'items', 'status', 'created_at', 'total']
        read_only_fields = ['order_code', 'created_at']

    def get_total(self, obj):
        return obj.total()

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)
        
        if not cart_items.exists():
            raise serializers.ValidationError("No items in the cart to create an order.")
        
        order = Order.objects.create(user=user, **validated_data)
        order.items.set(cart_items)
        
        # Clear the user's cart after creating the order
        cart_items.delete()
        
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class TransactionSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'order', 'order_id']

    def create(self, validated_data):
        order = validated_data.pop('order_id')
        transaction = Transaction.objects.create(order=order, **validated_data)
        return transaction

    def update(self, instance, validated_data):
        if 'order_id' in validated_data:
            instance.order = validated_data['order_id']
        instance.save()
        return instance