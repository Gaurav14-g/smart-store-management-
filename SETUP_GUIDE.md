# Smart Store Management System - Setup Guide

## System Requirements

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ (or MySQL 8+)
- Redis (for WebSocket support)

---

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd smart_store_be/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Edit `.env` file:
```env
# Database Configuration
USE_LOCAL=true
USE_DEV=false
USE_STAGE=false
USE_PROD=false

# Local Database Credentials
L_USER=your_db_user
L_HOST=localhost
L_PORT=5432
L_DB=smart_store_db
L_PASS=your_password

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
PAGE_SIZE=10

# Email Configuration (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles
STATICFILES_DIRS_PATH=static
```

### 5. Create Database
```bash
# PostgreSQL
createdb smart_store_db

# Or MySQL
mysql -u root -p
CREATE DATABASE smart_store_db;
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Create Roles
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create Admin Role
admin_group = Group.objects.create(name='Admin')
admin_group.permissions.set(Permission.objects.all())

# Create Staff Role
staff_group = Group.objects.create(name='Staff')
product_ct = ContentType.objects.get(app_label='api', model='product')
customer_ct = ContentType.objects.get(app_label='api', model='customer')
bill_ct = ContentType.objects.get(app_label='api', model='bill')

staff_permissions = Permission.objects.filter(
    content_type__in=[product_ct, customer_ct, bill_ct]
)
staff_group.permissions.set(staff_permissions)
exit()
```

### 9. Seed Test Data (Optional)
```bash
# Seed products
python manage.py seed_product 20

# Seed customers
python manage.py seed_customer 10

# Seed all
python manage.py seed_all 15
```

### 10. Start Development Server
```bash
python manage.py serve 0.0.0.0:8003
# Or
python manage.py runserver 0.0.0.0:8003
```

### 11. Access Backend
- API: http://localhost:8003/api/v1/
- Swagger: http://localhost:8003/api/v1/swagger/
- Admin: http://localhost:8003/admin/

---

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd smart_store_fe
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure API Endpoint
Edit `config/Global.json`:
```json
{
  "api": {
    "host": "http://127.0.0.1:8003",
    "token": "/auth/token/",
    "refreshToken": "/auth/token/refresh/",
    "product": "/api/v1/product/",
    "customer": "/api/v1/customer/",
    "bill": "/api/v1/bill/"
  }
}
```

### 4. Start Development Server
```bash
npm run dev
```

### 5. Access Frontend
- Application: http://localhost:5173/

---

## Testing

### Backend Tests
```bash
cd smart_store_be/backend
python manage.py test
```

### Test User Credentials
After seeding or manual creation:
- **Admin:** username: `admin`, password: `admin123`
- **Staff:** username: `staff1`, password: `staff123`

---

## Production Deployment

### Backend (Django)

1. **Update Settings**
```env
DEBUG=False
USE_PROD=true
```

2. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

3. **Use Production Server**
```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8003
```

4. **Setup Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Frontend (React)

1. **Build Production Bundle**
```bash
npm run build
```

2. **Deploy to Server**
```bash
# Copy dist folder to web server
scp -r dist/* user@server:/var/www/html/
```

3. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-frontend-domain.com;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## Docker Deployment (Optional)

### Backend Dockerfile
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8003"]
```

### Frontend Dockerfile
```dockerfile
FROM node:16 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

### Docker Compose
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: smart_store_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./smart_store_be/backend
    ports:
      - "8003:8003"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/smart_store_db

  frontend:
    build: ./smart_store_fe
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## Troubleshooting

### Database Connection Error
- Check database credentials in `.env`
- Ensure database server is running
- Verify database exists

### Migration Errors
```bash
python manage.py migrate --run-syncdb
```

### Port Already in Use
```bash
# Kill process on port 8003
lsof -ti:8003 | xargs kill -9
```

### CORS Errors
- Ensure `CORS_ALLOW_ALL_ORIGINS = True` in settings
- Or configure specific origins

---

## Maintenance

### Backup Database
```bash
# PostgreSQL
pg_dump smart_store_db > backup.sql

# MySQL
mysqldump -u root -p smart_store_db > backup.sql
```

### Restore Database
```bash
# PostgreSQL
psql smart_store_db < backup.sql

# MySQL
mysql -u root -p smart_store_db < backup.sql
```

### Update Dependencies
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```
