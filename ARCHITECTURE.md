# Smart Store Management System - Architecture Overview

## System Architecture

### Architecture Type
**Client-Server Architecture with REST API**

```
┌─────────────────┐         HTTP/REST         ┌─────────────────┐
│                 │ ◄────────────────────────► │                 │
│  React Frontend │                            │  Django Backend │
│   (Port 5173)   │                            │   (Port 8003)   │
│                 │                            │                 │
└─────────────────┘                            └────────┬────────┘
                                                        │
                                                        │ ORM
                                                        ▼
                                               ┌─────────────────┐
                                               │   PostgreSQL    │
                                               │    Database     │
                                               └─────────────────┘
```

---

## Technology Stack

### Backend
- **Framework:** Django 4.x + Django REST Framework
- **Language:** Python 3.8+
- **Database:** PostgreSQL (or MySQL)
- **Authentication:** JWT (Simple JWT)
- **API Documentation:** drf-yasg (Swagger)
- **Permissions:** Role-based Access Control (RBAC)

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **State Management:** Context API
- **UI Components:** Custom component library

### Database
- **Primary:** PostgreSQL 12+
- **ORM:** Django ORM
- **Migrations:** Django Migrations

---

## Database Schema

### ER Diagram

```
┌──────────────┐
│     USER     │
├──────────────┤
│ id (PK)      │
│ username     │
│ password     │
│ role         │
└──────┬───────┘
       │
       │ 1:N
       │
       ▼
┌──────────────┐         N:1         ┌──────────────┐
│     BILL     │◄────────────────────┤   CUSTOMER   │
├──────────────┤                     ├──────────────┤
│ id (PK)      │                     │ id (PK)      │
│ bill_date    │                     │ name         │
│ total_amount │                     │ phone        │
│ user_id (FK) │                     └──────────────┘
│ customer_id  │
└──────┬───────┘
       │
       │ 1:N
       │
       ▼
┌──────────────┐         N:1         ┌──────────────┐
│  BILL_ITEM   │────────────────────►│   PRODUCT    │
├──────────────┤                     ├──────────────┤
│ id (PK)      │                     │ id (PK)      │
│ bill_id (FK) │                     │ product_name │
│ product_id   │                     │ price        │
│ quantity     │                     │ quantity     │
│ price        │                     └──────────────┘
└──────────────┘
```

### Table Relationships

1. **USER → BILL** (1:N)
   - One user can create many bills
   - Foreign Key: `bill.user_id`

2. **CUSTOMER → BILL** (1:N)
   - One customer can have many bills
   - Foreign Key: `bill.customer_id`
   - Optional relationship (walk-in customers)

3. **BILL → BILL_ITEM** (1:N)
   - One bill contains many items
   - Foreign Key: `bill_item.bill_id`
   - Cascade delete

4. **PRODUCT → BILL_ITEM** (1:N)
   - One product can be in many bill items
   - Foreign Key: `bill_item.product_id`

---

## System Flow

### 1. Authentication Flow

```
User → Login Form → POST /auth/token/
                         ↓
                    Validate Credentials
                         ↓
                    Generate JWT Token
                         ↓
                    Return Access + Refresh Token
                         ↓
                    Store in LocalStorage
                         ↓
                    Redirect to Dashboard
```

### 2. Billing Flow

```
Staff → Select Customer (Optional)
            ↓
        Add Products to Cart
            ↓
        Specify Quantities
            ↓
        Review Total Amount
            ↓
        Submit Bill → POST /api/v1/bill/
            ↓
        Backend Validation:
        - Check stock availability
        - Validate quantities
        - Calculate total
            ↓
        Database Transaction:
        - Create Bill record
        - Create BillItem records
        - Deduct product stock
        - Commit or Rollback
            ↓
        Return Bill with Invoice
            ↓
        Display Success Message
```

### 3. Product Management Flow

```
Admin → Product List → View/Search/Filter
            ↓
        Select Action:
        ├─ Create → Form → POST /api/v1/product/
        ├─ Update → Form → PUT /api/v1/product/{id}/
        └─ Delete → Confirm → DELETE /api/v1/product/{id}/
            ↓
        Backend Processing:
        - Validate input
        - Check permissions
        - Update database
            ↓
        Return Response
            ↓
        Refresh Product List
```

---

## Layered Architecture

### Backend Layers

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│  (Views, Serializers, URLs)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Business Logic Layer        │
│  (ViewSets, Permissions, Services)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data Access Layer           │
│  (Models, ORM, Database)            │
└─────────────────────────────────────┘
```

### Frontend Layers

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│  (Pages, Components, UI)            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Application Layer           │
│  (Hooks, Context, State)            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data Layer                  │
│  (API Calls, Models, Types)         │
└─────────────────────────────────────┘
```

---

## Security Architecture

### Authentication
- JWT-based authentication
- Access token (5 min expiry)
- Refresh token (1 day expiry)
- Token rotation on refresh
- Blacklist on logout

### Authorization
- Role-Based Access Control (RBAC)
- Django Groups and Permissions
- Custom permission classes
- Endpoint-level protection

### Data Security
- Password hashing (PBKDF2)
- SQL injection prevention (ORM)
- XSS protection (React escaping)
- CSRF protection (Django middleware)
- CORS configuration

---

## API Design

### RESTful Principles
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Stateless communication
- JSON data format
- Standard HTTP status codes

### Endpoint Structure
```
/api/v1/{resource}/
/api/v1/{resource}/{id}/
/api/v1/{resource}/{action}/
```

### Response Format
```json
{
  "count": 100,
  "next": "url",
  "previous": "url",
  "results": []
}
```

---

## Folder Structure

### Backend Structure
```
backend/
├── api/
│   ├── Product/
│   │   ├── model.py
│   │   ├── serializer.py
│   │   └── view.py
│   ├── Customer/
│   ├── Bill/
│   ├── User/
│   ├── Role/
│   ├── Permission/
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── apps.py
│   ├── urls.py
│   └── permissions.py
├── backend/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── security/
├── manage.py
└── requirements.txt
```

### Frontend Structure
```
src/
├── components/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── CrudManager.tsx
│   └── ...
├── pages/
│   ├── admin/
│   │   ├── Products.tsx
│   │   ├── Customers.tsx
│   │   ├── Billing.tsx
│   │   └── SalesReports.tsx
│   └── auth/
├── models/
│   ├── Product.ts
│   ├── Customer.ts
│   └── Bill.ts
├── hooks/
│   └── useApi.ts
├── context/
│   └── AuthContext.tsx
├── layouts/
│   └── AdminLayout.tsx
└── App.tsx
```

---

## Design Patterns

### Backend Patterns
1. **MVC Pattern** - Model-View-Controller separation
2. **Repository Pattern** - Data access abstraction
3. **Serializer Pattern** - Data transformation
4. **ViewSet Pattern** - CRUD operations
5. **Middleware Pattern** - Request/response processing

### Frontend Patterns
1. **Component Pattern** - Reusable UI components
2. **Container Pattern** - Smart vs Dumb components
3. **Hook Pattern** - Reusable logic
4. **Context Pattern** - Global state management
5. **HOC Pattern** - PrivateRoute wrapper

---

## Scalability Considerations

### Current Implementation
- Single server deployment
- Monolithic architecture
- Direct database connection

### Future Enhancements
- Load balancing
- Database replication
- Caching layer (Redis)
- Microservices architecture
- Message queue (Celery)
- CDN for static files

---

## Performance Optimization

### Backend
- Database indexing
- Query optimization
- Select/prefetch related
- Pagination
- Connection pooling

### Frontend
- Code splitting
- Lazy loading
- Memoization
- Virtual scrolling
- Asset optimization

---

## Monitoring & Logging

### Backend Logging
- Django logging framework
- Error tracking
- Request/response logging
- Database query logging

### Frontend Logging
- Console logging
- Error boundaries
- API error tracking

---

## Backup & Recovery

### Database Backup
- Daily automated backups
- Point-in-time recovery
- Backup retention policy

### Application Backup
- Version control (Git)
- Configuration backups
- Static file backups
