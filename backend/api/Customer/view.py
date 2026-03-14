from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, Q
from datetime import datetime, timedelta
from .model import Customer
from .serializer import CustomerSerializer
from api.Bill.model import Bill, BillItem

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        customer = self.get_object()
        bills = Bill.objects.filter(customer=customer)
        
        total_spent = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_purchases = bills.count()
        avg_purchase = bills.aggregate(Avg('total_amount'))['total_amount__avg'] or 0
        
        last_purchase = bills.order_by('-bill_date').first()
        last_purchase_date = last_purchase.bill_date if last_purchase else None
        
        top_products = BillItem.objects.filter(
            bill__customer=customer
        ).values('product__product_name').annotate(
            qty=Sum('quantity'),
            spent=Sum('price')
        ).order_by('-qty')[:5]
        
        return Response({
            'customer_id': str(customer.id),
            'customer_name': customer.name,
            'total_spent': float(total_spent),
            'total_purchases': total_purchases,
            'avg_purchase_value': float(avg_purchase),
            'last_purchase_date': last_purchase_date,
            'top_products': list(top_products),
            'purchase_frequency': self._calculate_frequency(bills)
        })
    
    @action(detail=False, methods=['get'])
    def top_customers(self, request):
        limit = int(request.query_params.get('limit', 10))
        
        customers_data = []
        for customer in Customer.objects.all():
            bills = Bill.objects.filter(customer=customer)
            total_spent = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            if total_spent > 0:
                customers_data.append({
                    'id': str(customer.id),
                    'name': customer.name,
                    'phone': customer.phone,
                    'total_spent': float(total_spent),
                    'purchase_count': bills.count()
                })
        
        customers_data.sort(key=lambda x: x['total_spent'], reverse=True)
        return Response(customers_data[:limit])
    
    def _calculate_frequency(self, bills):
        if bills.count() < 2:
            return 'New'
        
        last_30_days = datetime.now() - timedelta(days=30)
        recent = bills.filter(bill_date__gte=last_30_days).count()
        
        if recent >= 5:
            return 'Very Active'
        elif recent >= 2:
            return 'Active'
        else:
            return 'Inactive'
