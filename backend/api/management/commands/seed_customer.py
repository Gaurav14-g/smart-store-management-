from django.core.management.base import BaseCommand
from api.Customer.model import Customer
from faker import Faker

class Command(BaseCommand):
    help = 'Seed Customer data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of customers to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()
        
        for _ in range(count):
            Customer.objects.create(
                name=fake.name(),
                phone=fake.phone_number()[:15]
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} customers'))
