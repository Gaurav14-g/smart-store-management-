from rest_framework import serializers
from .model import Bill, BillItem
from api.Product.model import Product
from django.db import transaction

class BillItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = BillItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = ['id', 'price']

class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Bill
        fields = ['id', 'bill_date', 'total_amount', 'user', 'user_name', 'customer', 'customer_name', 'items', 'created_at']
        read_only_fields = ['id', 'bill_date', 'total_amount', 'user', 'created_at']
    
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        if not items_data:
            raise serializers.ValidationError("Bill must have at least one item")
        
        total_amount = 0
        bill_items = []
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            if quantity <= 0:
                raise serializers.ValidationError(f"Quantity must be positive for {product.product_name}")
            
            if product.quantity < quantity:
                raise serializers.ValidationError(f"Insufficient stock for {product.product_name}. Available: {product.quantity}")
            
            price = product.price
            total_amount += price * quantity
            bill_items.append({
                'product': product,
                'quantity': quantity,
                'price': price
            })
        
        bill = Bill.objects.create(
            user=user,
            customer=validated_data.get('customer'),
            total_amount=total_amount
        )
        
        for item in bill_items:
            BillItem.objects.create(
                bill=bill,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )
            item['product'].quantity -= item['quantity']
            item['product'].save()
        
        return bill

class BillListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Bill
        fields = ['id', 'bill_date', 'total_amount', 'user_name', 'customer_name', 'items_count']
