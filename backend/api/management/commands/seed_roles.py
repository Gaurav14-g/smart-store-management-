from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Seed store roles: Owner, Manager, Cashier, Employee'

    def handle(self, *args, **kwargs):
        # All model permissions we care about
        models = ['product', 'customer', 'bill', 'billitem', 'user']
        actions = ['view', 'add', 'change', 'delete']

        def get_perms(*pairs):
            """pairs = [('view','product'), ('add','bill'), ...]"""
            result = []
            for action, model in pairs:
                try:
                    result.append(Permission.objects.get(codename=f'{action}_{model}'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permission {action}_{model} not found, skipping'))
            return result

        roles = {
            'Owner': get_perms(
                ('view', 'product'), ('add', 'product'), ('change', 'product'), ('delete', 'product'),
                ('view', 'customer'), ('add', 'customer'), ('change', 'customer'), ('delete', 'customer'),
                ('view', 'bill'), ('add', 'bill'), ('change', 'bill'), ('delete', 'bill'),
                ('view', 'billitem'), ('add', 'billitem'), ('change', 'billitem'), ('delete', 'billitem'),
                ('view', 'user'), ('add', 'user'), ('change', 'user'), ('delete', 'user'),
            ),
            'Manager': get_perms(
                ('view', 'product'), ('add', 'product'), ('change', 'product'),
                ('view', 'customer'), ('add', 'customer'), ('change', 'customer'),
                ('view', 'bill'), ('add', 'bill'),
                ('view', 'billitem'), ('add', 'billitem'),
                ('view', 'user'),
            ),
            'Cashier': get_perms(
                ('view', 'product'),
                ('view', 'customer'), ('add', 'customer'),
                ('view', 'bill'), ('add', 'bill'),
                ('view', 'billitem'), ('add', 'billitem'),
            ),
            'Employee': get_perms(
                ('view', 'product'),
                ('view', 'customer'),
                ('view', 'bill'),
                ('view', 'billitem'),
            ),
        }

        for role_name, perms in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            group.permissions.set(perms)
            group.save()
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action} role: {role_name} ({len(perms)} permissions)'))

        self.stdout.write(self.style.SUCCESS('\nDone! Roles seeded successfully.'))
        self.stdout.write('Run: python manage.py seed_roles')
