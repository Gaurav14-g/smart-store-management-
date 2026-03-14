from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .model import Product
from .serializer import ProductSerializer

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product_name', 'upc']
    search_fields = ['product_name', 'upc']
    ordering_fields = ['created_at', 'product_name', 'price', 'quantity']
    
    @action(detail=False, methods=['get'], url_path='scan/(?P<upc>[^/.]+)')
    def scan(self, request, upc=None):
        try:
            product = Product.objects.get(upc=upc)
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def check_stock(self, request):
        items = request.data.get('items', [])
        errors = []
        
        for item in items:
            product_id = item.get('product')
            quantity = item.get('quantity', 0)
            
            try:
                product = Product.objects.get(id=product_id)
                if product.quantity < quantity:
                    errors.append(f"{product.product_name}: Only {product.quantity} available")
            except Product.DoesNotExist:
                errors.append(f"Product {product_id} not found")
        
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'ok'})
