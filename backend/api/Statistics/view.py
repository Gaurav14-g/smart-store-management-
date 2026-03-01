from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from api.Product.model import Product
from api.Customer.model import Customer
from api.Bill.model import Bill

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistics(request):
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_bills = Bill.objects.count()
    total_revenue = Bill.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    low_stock_products = Product.objects.filter(quantity__lt=10).count()
    
    recent_bills = Bill.objects.order_by('-bill_date')[:5].values(
        'id', 'bill_date', 'total_amount', 'customer__name'
    )
    
    return Response({
        'total_products': total_products,
        'total_customers': total_customers,
        'total_bills': total_bills,
        'total_revenue': float(total_revenue),
        'low_stock_products': low_stock_products,
        'recent_bills': list(recent_bills)
    })
