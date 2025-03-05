from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'status', 'created_at', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)

        for item in order_items_data:
            OrderItem.objects.create(order=order, **item)
        return order
