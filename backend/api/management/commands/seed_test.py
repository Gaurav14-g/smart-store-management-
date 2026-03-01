from django.core.management.base import BaseCommand
from api.TestAPI.model import Test
import uuid
from faker import Faker

class Command(BaseCommand):
    help = 'Seed the Test model with n records'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of records to create')

    def handle(self, *args, **kwargs):
        n = kwargs['n']
        faker = Faker()

        for _ in range(n):
            Test.objects.create(
                id=uuid.uuid4(),
                name=faker.name(),
                description=faker.text(max_nb_chars=200),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {n} records into Test model'))
