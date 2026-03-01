# django-placeholder

## How to Run This Project

### 1. Setup Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database
Edit `backend/.env` and set ONE database flag to `true`:
```env
USE_LOCAL=true   # Use local database
USE_DEV=false    # Use development database
USE_STAGE=false  # Use stage database
USE_PROD=false   # Use production database
```

Configure your database credentials:
```env
L_USER=humbingo
L_HOST=localhost
L_PORT=5432
L_DB=django_placeholder
L_PASS=Welcome@1
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Data (Optional)
```bash
python manage.py seed_test 3      # Generate 3 test records
python manage.py seed_all 5       # Generate 5 records for all models
```

### 5. Start Server
```bash
# Using custom serve command (with ASCII banner)
python manage.py serve 0.0.0.0:8003

# Or using default runserver
python manage.py runserver 0.0.0.0:8003
```

### 6. Access Application
- Health Check: http://localhost:8003/
- API: http://localhost:8003/api/v1/
- Swagger: http://localhost:8003/api/v1/swagger/
- Admin: http://localhost:8003/admin/

---

## Project Features

Roles
- Superuser
- Backoffice
- User

Remember
- add new model in apps.py of app
- new seed file is must listed in seed_all file in sequence


django-placehoder includes
- .env (local, development, stage, production)
- requirements.txt
- Test api and address api both connected with FK
- filter
- swagger
- permissions, roles
- security app(for token and authentication)
- seed data and fakers
- display reference name for FK (code is in serializer)
- CORS header and pagination
- static files
- changeMyPassword
- forget password (some changes must requires, 1- settings.py change email id and application password. from that mail link will be sent. 2- view.py change server link http://127.0.0.1:8001/)
- checkUserUser
- userProfile with contact_no field which is associated with user model
- createUser without authentication
- websocket - django channels (base.py, asgi.py, api/websocket (routings.py works like urls.py and consumers.py works like views.py))


seed_files
- api/management/commands (python manage.py seed_test 3) <-- it will generate 3 records for test model. (python manage.py seed_all 5) <-- it will generate 5 records for all models.


