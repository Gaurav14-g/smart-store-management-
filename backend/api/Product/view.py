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
