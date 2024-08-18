from rest_framework import serializers
from order import OrderSerializer
from models.payment import Payment
from models.order import Order

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        order = Order.objects.create(**order_data)
        payment = Payment.objects.create(order=order, **validated_data)
        return payment

    def update(self, instance, validated_data):
        order_data = validated_data.pop('order')
        order = instance.order

        instance.amount = validated_data.get('amount', instance.amount)
        instance.status = validated_data.get('status', instance.status)
        instance.reference_id = validated_data.get('reference_id', instance.reference_id)
        instance.save()

        order.order_code = order_data.get('order_code', order.order_code)
        order.save()

        return instance
