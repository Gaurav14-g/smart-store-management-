from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from datetime import datetime
from .model import Bill
from .serializer import BillSerializer, BillListSerializer

class BillViewset(viewsets.ModelViewSet):
    queryset = Bill.objects.all().select_related('user', 'customer').prefetch_related('items__product')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'customer', 'bill_date']
    search_fields = ['customer__name', 'user__username']
    ordering_fields = ['bill_date', 'total_amount']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BillListSerializer
        return BillSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'], url_path='sales-report')
    def sales_report(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.get_queryset()
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(bill_date__gte=start_date)
            except ValueError:
                return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(bill_date__lte=end_date)
            except ValueError:
                return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_sales = queryset.aggregate(
            total_amount=Sum('total_amount'),
            total_bills=Count('id')
        )
        
        bills = BillListSerializer(queryset, many=True).data
        
        return Response({
            'summary': {
                'total_sales': total_sales['total_amount'] or 0,
                'total_bills': total_sales['total_bills'] or 0,
                'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
                'end_date': end_date.strftime('%Y-%m-%d') if end_date else None
            },
            'bills': bills
        })
