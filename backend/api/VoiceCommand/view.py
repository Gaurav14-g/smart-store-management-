from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from api.Product.model import Product
from api.Customer.model import Customer
from api.Bill.model import Bill
from .parser import VoiceCommandParser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def voice_command(request):
    text = request.data.get('command', '').lower()
    parser = VoiceCommandParser()
    
    # Try to parse add product command
    product_data = parser.parse_add_product(text)
    if product_data:
        try:
            product = Product.objects.create(
                product_name=product_data['product_name'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            return Response({
                'action': 'add_product',
                'message': f'Product "{product_data["product_name"]}" added successfully',
                'product_id': str(product.id),
                'success': True
            })
        except Exception as e:
            return Response({
                'action': 'add_product',
                'message': f'Error: {str(e)}',
                'success': False
            }, status=400)
    
    elif parser.parse_update_product(text):
        update_data = parser.parse_update_product(text)
        product = Product.objects.filter(product_name__icontains=update_data['product_name']).first()
        if product:
            if update_data['price']:
                product.price = update_data['price']
            if update_data['quantity']:
                product.quantity = update_data['quantity']
            product.save()
            return Response({
                'action': 'update_product',
                'message': f'Product "{product.product_name}" updated successfully',
                'success': True
            })
        return Response({
            'action': 'update_product',
            'message': f'Product "{update_data["product_name"]}" not found',
            'success': False
        }, status=404)
    
    elif parser.parse_check_stock(text):
        low_stock = Product.objects.filter(quantity__lt=10)
        product_list = ', '.join([f'{p.product_name} with {p.quantity} in stock' for p in low_stock])
        message = f'Low stock alert. {product_list}' if low_stock else 'All products have sufficient stock'
        return Response({
            'action': 'check_stock',
            'low_stock_count': low_stock.count(),
            'products': [
                {'name': p.product_name, 'quantity': p.quantity}
                for p in low_stock
            ],
            'message': message
        })
    
    elif parser.parse_generate_report(text):
        total_revenue = Bill.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        total_bills = Bill.objects.count()
        message = f'Total revenue is {total_revenue} from {total_bills} bills'
        return Response({
            'action': 'generate_report',
            'total_revenue': float(total_revenue),
            'total_bills': total_bills,
            'message': message
        })
    
    elif parser.parse_show_statistics(text):
        total_products = Product.objects.count()
        total_customers = Customer.objects.count()
        low_stock = Product.objects.filter(quantity__lt=10).count()
        message = f'We have {total_products} products, {total_customers} customers, and {low_stock} products with low stock'
        return Response({
            'action': 'show_statistics',
            'total_products': total_products,
            'total_customers': total_customers,
            'low_stock_products': low_stock,
            'message': message
        })
    
    elif parser.parse_complete_sale(text):
        return Response({
            'action': 'complete_sale',
            'message': 'Ready to complete sale'
        })
    
    elif parser.parse_clear_cart(text):
        return Response({
            'action': 'clear_cart',
            'message': 'Cart cleared'
        })
    
    elif parser.parse_list_products(text):
        products = Product.objects.all()
        product_list = ', '.join([f'{p.product_name} with {p.quantity} in stock' for p in products])
        message = f'Found {products.count()} products. {product_list}' if products else 'No products found'
        return Response({
            'action': 'list_products',
            'total_products': products.count(),
            'products': [
                {'name': p.product_name, 'stock': p.quantity, 'price': float(p.price)}
                for p in products
            ],
            'message': message
        })
    
    elif parser.parse_product_details(text):
        product_name = parser.parse_product_details(text)
        product = Product.objects.filter(product_name__icontains=product_name).first()
        if product:
            return Response({
                'action': 'product_details',
                'name': product.product_name,
                'price': float(product.price),
                'stock': product.quantity,
                'message': f'{product.product_name} costs {product.price} and we have {product.quantity} in stock'
            })
        return Response({
            'action': 'product_details',
            'message': f'Product {product_name} not found',
            'success': False
        }, status=404)
    
    elif parser.parse_low_stock_alert(text):
        low_stock = Product.objects.filter(quantity__lt=10)
        product_list = ', '.join([f'{p.product_name} with {p.quantity} in stock' for p in low_stock])
        message = f'We have {low_stock.count()} products with low stock. {product_list}' if low_stock else 'All products have sufficient stock'
        return Response({
            'action': 'low_stock_alert',
            'count': low_stock.count(),
            'products': [
                {'name': p.product_name, 'stock': p.quantity}
                for p in low_stock
            ],
            'message': message
        })
    
    else:
        return Response({
            'action': 'unknown',
            'message': 'Command not recognized. Say: "add product [name] price [price]"',
            'success': False
        }, status=400)
