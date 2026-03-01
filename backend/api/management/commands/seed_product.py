from django.core.management.base import BaseCommand
from api.Product.model import Product
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed Product data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of products to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()
        
        products = [
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
            'Smartphone', 'Tablet', 'Charger', 'USB Cable', 'Hard Drive',
            'SSD', 'RAM', 'Graphics Card', 'Processor', 'Motherboard',
            'Power Supply', 'Case', 'Cooling Fan', 'Webcam', 'Microphone'
        ]
        
        for _ in range(count):
            Product.objects.create(
                product_name=random.choice(products) + ' ' + fake.word().capitalize(),
                price=round(random.uniform(10, 1000), 2),
                quantity=random.randint(0, 100)
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} products'))
