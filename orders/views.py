
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderListCreateAPIView(APIView):
    def get(self, request):
        orders = Order.objects.prefetch_related('order_items').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            order_items = request.data.get('order_items', [])
            errors = []

            for item in order_items:
                item_serializer = OrderItemSerializer(data=item)
                if item_serializer.is_valid():
                    item_serializer.save(order=order)
                else:
                    errors.append(item_serializer.errors)

            if errors:
                return Response({'order_items_errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
