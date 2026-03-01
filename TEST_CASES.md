# Smart Store Management System - Test Cases

## Unit Tests

### Product Model Tests

```python
# backend/api/Product/tests.py
from django.test import TestCase
from api.Product.model import Product
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name="Test Product",
            price=Decimal('100.00'),
            quantity=10
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.product_name, "Test Product")
        self.assertEqual(self.product.price, Decimal('100.00'))
        self.assertEqual(self.product.quantity, 10)
    
    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")
    
    def test_negative_quantity_validation(self):
        product = Product(
            product_name="Invalid Product",
            price=Decimal('50.00'),
            quantity=-5
        )
        with self.assertRaises(Exception):
            product.full_clean()
```

### Customer Model Tests

```python
# backend/api/Customer/tests.py
from django.test import TestCase
from api.Customer.model import Customer

class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create(
            name="John Doe",
            phone="1234567890"
        )
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.phone, "1234567890")
    
    def test_customer_str(self):
        customer = Customer.objects.create(
            name="Jane Smith",
            phone="9876543210"
        )
        self.assertEqual(str(customer), "Jane Smith")
```

### Bill Model Tests

```python
# backend/api/Bill/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from api.Bill.model import Bill, BillItem
from api.Product.model import Product
from api.Customer.model import Customer
from decimal import Decimal

class BillModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            name="Test Customer",
            phone="1234567890"
        )
        self.product = Product.objects.create(
            product_name="Test Product",
            price=Decimal('100.00'),
            quantity=10
        )
    
    def test_bill_creation(self):
        bill = Bill.objects.create(
            user=self.user,
            customer=self.customer,
            total_amount=Decimal('200.00')
        )
        self.assertEqual(bill.user, self.user)
        self.assertEqual(bill.customer, self.customer)
        self.assertEqual(bill.total_amount, Decimal('200.00'))
    
    def test_bill_item_creation(self):
        bill = Bill.objects.create(
            user=self.user,
            total_amount=Decimal('100.00')
        )
        bill_item = BillItem.objects.create(
            bill=bill,
            product=self.product,
            quantity=1,
            price=Decimal('100.00')
        )
        self.assertEqual(bill_item.bill, bill)
        self.assertEqual(bill_item.product, self.product)
        self.assertEqual(bill_item.quantity, 1)
```

---

## API Integration Tests

### Authentication Tests

```python
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_success(self):
        response = self.client.post('/auth/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        response = self.client.post('/auth/token/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh(self):
        login_response = self.client.post('/auth/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        refresh_token = login_response.data['refresh']
        
        response = self.client.post('/auth/token/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
```

### Product API Tests

```python
class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            product_name="Test Product",
            price=Decimal('100.00'),
            quantity=10
        )
    
    def test_list_products(self):
        response = self.client.get('/api/v1/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_product(self):
        data = {
            'product_name': 'New Product',
            'price': 50.00,
            'quantity': 20
        }
        response = self.client.post('/api/v1/product/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
    
    def test_create_product_invalid_price(self):
        data = {
            'product_name': 'Invalid Product',
            'price': -10.00,
            'quantity': 5
        }
        response = self.client.post('/api/v1/product/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_product(self):
        data = {
            'product_name': 'Updated Product',
            'price': 150.00,
            'quantity': 15
        }
        response = self.client.put(
            f'/api/v1/product/{self.product.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.product_name, 'Updated Product')
    
    def test_delete_product(self):
        response = self.client.delete(f'/api/v1/product/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
```

### Billing API Tests

```python
class BillingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(
            name="Test Customer",
            phone="1234567890"
        )
        self.product1 = Product.objects.create(
            product_name="Product 1",
            price=Decimal('100.00'),
            quantity=10
        )
        self.product2 = Product.objects.create(
            product_name="Product 2",
            price=Decimal('50.00'),
            quantity=20
        )
    
    def test_create_bill_success(self):
        data = {
            'customer': str(self.customer.id),
            'items': [
                {
                    'product': str(self.product1.id),
                    'quantity': 2
                },
                {
                    'product': str(self.product2.id),
                    'quantity': 1
                }
            ]
        }
        response = self.client.post('/api/v1/bill/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bill.objects.count(), 1)
        
        # Check stock deduction
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.quantity, 8)
        self.assertEqual(self.product2.quantity, 19)
    
    def test_create_bill_insufficient_stock(self):
        data = {
            'items': [
                {
                    'product': str(self.product1.id),
                    'quantity': 20  # More than available
                }
            ]
        }
        response = self.client.post('/api/v1/bill/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_bill_without_items(self):
        data = {
            'customer': str(self.customer.id),
            'items': []
        }
        response = self.client.post('/api/v1/bill/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_bills(self):
        Bill.objects.create(
            user=self.user,
            customer=self.customer,
            total_amount=Decimal('100.00')
        )
        response = self.client.get('/api/v1/bill/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Sales Report Tests

```python
class SalesReportAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test bills
        Bill.objects.create(
            user=self.user,
            total_amount=Decimal('100.00')
        )
        Bill.objects.create(
            user=self.user,
            total_amount=Decimal('200.00')
        )
    
    def test_sales_report_all(self):
        response = self.client.get('/api/v1/bill/sales-report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_bills'], 2)
        self.assertEqual(
            response.data['summary']['total_sales'],
            Decimal('300.00')
        )
    
    def test_sales_report_date_filter(self):
        response = self.client.get(
            '/api/v1/bill/sales-report/',
            {'start_date': '2024-01-01', 'end_date': '2024-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

---

## Frontend Test Cases

### Component Tests (Jest + React Testing Library)

```typescript
// Products.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Products from './Products';
import { BrowserRouter } from 'react-router-dom';

describe('Products Component', () => {
  test('renders product list', async () => {
    render(
      <BrowserRouter>
        <Products />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Products')).toBeInTheDocument();
    });
  });
  
  test('opens create product form', () => {
    render(
      <BrowserRouter>
        <Products />
      </BrowserRouter>
    );
    
    const createButton = screen.getByText('Add Product');
    fireEvent.click(createButton);
    
    expect(screen.getByText('Create Product')).toBeInTheDocument();
  });
});
```

### API Hook Tests

```typescript
// useApi.test.ts
import { renderHook } from '@testing-library/react-hooks';
import useApi from './useApi';
import axios from 'axios';

jest.mock('axios');

describe('useApi Hook', () => {
  test('Get request returns data', async () => {
    const mockData = { results: [] };
    (axios.get as jest.Mock).mockResolvedValue({ data: mockData });
    
    const { result } = renderHook(() => useApi());
    const data = await result.current.Get('product');
    
    expect(data).toEqual(mockData);
  });
});
```

---

## Manual Test Cases

### Test Case 1: User Login
**Precondition:** User exists in database
**Steps:**
1. Navigate to login page
2. Enter username and password
3. Click login button

**Expected Result:** User redirected to dashboard with success message

---

### Test Case 2: Create Product
**Precondition:** User logged in as Admin
**Steps:**
1. Navigate to Products page
2. Click "Add Product" button
3. Fill in product details
4. Click "Save"

**Expected Result:** Product created and appears in list

---

### Test Case 3: Generate Bill
**Precondition:** Products exist with stock
**Steps:**
1. Navigate to Billing page
2. Select customer (optional)
3. Add products with quantities
4. Click "Generate Bill"

**Expected Result:** 
- Bill created successfully
- Stock deducted
- Invoice displayed

---

### Test Case 4: Insufficient Stock
**Precondition:** Product has limited stock
**Steps:**
1. Navigate to Billing page
2. Add product with quantity > available stock
3. Click "Generate Bill"

**Expected Result:** Error message "Insufficient stock"

---

### Test Case 5: Sales Report
**Precondition:** Bills exist in database
**Steps:**
1. Navigate to Sales Reports
2. Select date range
3. Click "Generate Report"

**Expected Result:** Report shows total sales and bill list

---

## Performance Test Cases

### Load Testing
- **Test:** 100 concurrent users creating bills
- **Expected:** Response time < 2 seconds

### Stress Testing
- **Test:** 1000 products in database
- **Expected:** List loads in < 1 second

---

## Security Test Cases

### Test Case: SQL Injection
**Input:** `'; DROP TABLE product; --`
**Expected:** Input sanitized, no database damage

### Test Case: XSS Attack
**Input:** `<script>alert('XSS')</script>`
**Expected:** Script escaped, not executed

### Test Case: Unauthorized Access
**Steps:** Access protected endpoint without token
**Expected:** 401 Unauthorized response

---

## Run Tests

### Backend
```bash
cd backend
python manage.py test
```

### Frontend
```bash
cd frontend
npm test
```
