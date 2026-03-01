# Smart Store Management System - API Documentation

## Base URL
```
http://localhost:8003/api/v1/
```

## Authentication
All endpoints require JWT authentication except login.

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### 1. Login
**POST** `/auth/token/`

**Request:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Refresh Token
**POST** `/auth/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Product Management

### 1. List Products
**GET** `/api/v1/product/`

**Query Parameters:**
- `page`: Page number
- `search`: Search by product name
- `ordering`: Sort by field (e.g., `-created_at`, `price`)

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "product_name": "Laptop Dell XPS",
      "price": "1200.00",
      "quantity": 10,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 2. Create Product
**POST** `/api/v1/product/`

**Request:**
```json
{
  "product_name": "Wireless Mouse",
  "price": 25.00,
  "quantity": 50
}
```

**Validation:**
- `product_name`: Required, max 200 chars
- `price`: Required, must be > 0
- `quantity`: Required, must be >= 0

### 3. Update Product
**PUT** `/api/v1/product/{id}/`

**Request:**
```json
{
  "product_name": "Wireless Mouse Pro",
  "price": 30.00,
  "quantity": 45
}
```

### 4. Delete Product
**DELETE** `/api/v1/product/{id}/`

**Response:** `204 No Content`

---

## Customer Management

### 1. List Customers
**GET** `/api/v1/customer/`

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": "uuid",
      "name": "John Doe",
      "phone": "1234567890",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 2. Create Customer
**POST** `/api/v1/customer/`

**Request:**
```json
{
  "name": "Jane Smith",
  "phone": "9876543210"
}
```

### 3. Update Customer
**PUT** `/api/v1/customer/{id}/`

### 4. Delete Customer
**DELETE** `/api/v1/customer/{id}/`

---

## Billing

### 1. Create Bill
**POST** `/api/v1/bill/`

**Request:**
```json
{
  "customer": "customer-uuid",
  "items": [
    {
      "product": "product-uuid",
      "quantity": 2
    },
    {
      "product": "product-uuid-2",
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": "bill-uuid",
  "bill_date": "2024-01-15T10:30:00Z",
  "total_amount": "2450.00",
  "user": "user-id",
  "user_name": "staff_user",
  "customer": "customer-uuid",
  "customer_name": "John Doe",
  "items": [
    {
      "id": "item-uuid",
      "product": "product-uuid",
      "product_name": "Laptop Dell XPS",
      "quantity": 2,
      "price": "1200.00"
    }
  ]
}
```

**Business Logic:**
- Validates stock availability
- Deducts stock automatically
- Calculates total amount
- Uses database transactions
- Prevents negative stock

**Error Responses:**
```json
{
  "items": ["Insufficient stock for Laptop Dell XPS. Available: 5"]
}
```

### 2. List Bills
**GET** `/api/v1/bill/`

**Query Parameters:**
- `user`: Filter by user ID
- `customer`: Filter by customer ID
- `bill_date`: Filter by date

### 3. Get Bill Details
**GET** `/api/v1/bill/{id}/`

---

## Sales Reports

### 1. Generate Sales Report
**GET** `/api/v1/bill/sales-report/`

**Query Parameters:**
- `start_date`: YYYY-MM-DD format
- `end_date`: YYYY-MM-DD format

**Example:**
```
GET /api/v1/bill/sales-report/?start_date=2024-01-01&end_date=2024-01-31
```

**Response:**
```json
{
  "summary": {
    "total_sales": 15000.00,
    "total_bills": 25,
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  },
  "bills": [
    {
      "id": "uuid",
      "bill_date": "2024-01-15T10:30:00Z",
      "total_amount": "2450.00",
      "user_name": "staff_user",
      "customer_name": "John Doe",
      "items_count": 3
    }
  ]
}
```

---

## User Management

### 1. List Users
**GET** `/api/v1/user/`

### 2. Create User
**POST** `/api/v1/user/`

**Request:**
```json
{
  "username": "staff1",
  "password": "secure_password",
  "email": "staff1@example.com",
  "first_name": "Staff",
  "last_name": "User",
  "groups": [2],
  "is_staff": true,
  "is_active": true
}
```

---

## Role Management

### 1. List Roles
**GET** `/api/v1/role/`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Admin"
  },
  {
    "id": 2,
    "name": "Staff"
  }
]
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Permissions

### Admin Role
- Full access to all endpoints
- View sales reports
- Manage products
- Manage users

### Staff Role
- Manage customers
- Create bills
- View products
- Limited user access

---

## Rate Limiting
No rate limiting implemented in Phase 1.

## Pagination
Default page size: 10 items
Can be configured in settings.

## Swagger Documentation
Available at: `http://localhost:8003/api/v1/swagger/`
