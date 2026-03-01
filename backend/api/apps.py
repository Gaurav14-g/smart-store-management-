from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.UserProfile
        import api.TestAPI.model
        import api.Product.model
        import api.Customer.model
        import api.Bill.model
        