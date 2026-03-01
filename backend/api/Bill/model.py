from django.db import models
from django.contrib.auth.models import User
from api.Customer.model import Customer
from api.Product.model import Product
import uuid

class Bill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bills', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bill'
        ordering = ['-bill_date']
        indexes = [
            models.Index(fields=['-bill_date']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"Bill {self.id} - {self.total_amount}"

class BillItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bill_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bill_item'
        indexes = [
            models.Index(fields=['bill']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f"BillItem {self.id} - {self.product.product_name}"
