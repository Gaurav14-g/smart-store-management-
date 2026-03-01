import os
import sys
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Run Django app with Daphne (WebSocket support)'

    def add_arguments(self, parser):
        parser.add_argument(
            'addrport', nargs='?', default='0.0.0.0:8000',
            help='Optional port number, or ipaddr:port'
        )

    def handle(self, *args, **options):
        load_dotenv(override=True)
        
        # Determine environment name
        env_name = "LOCAL"
        if os.getenv("USE_LOCAL") == "true":
            env_name = "LOCAL"
        elif os.getenv("USE_DEV") == "true":
            env_name = "DEVELOPMENT"
        elif os.getenv("USE_STAGE") == "true":
            env_name = "STAGE"
        elif os.getenv("USE_PROD") == "true":
            env_name = "PRODUCTION"
        
        # Get host and port from options
        addrport = options.get('addrport', '0.0.0.0:8000')
        
        # Parse address and port
        if ':' in addrport:
            host, port = addrport.split(':')
        else:
            host = '0.0.0.0'
            port = addrport
        
        # ASCII Art Banner
        banner = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗      ██║ █████╗ ███╗   ██╗ ██████╗  ██████╗   ║
║   ██╔══██╗     ██║██╔══██╗████╗  ██║██╔════╝ ██╔═══██╗  ║
║   ██║  ██║     ██║███████║██╔██╗ ██║██║  ███╗██║   ██║  ║
║   ██║  ██║██   ██║██╔══██║██║╚██╗██║██║   ██║██║   ██║  ║
║   ██████╔╝╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝  ║
║   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝   ║
║                                                           ║
║              Environment: {env_name:<20}          ║
║              Server: {host}:{port:<25}          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        
        self.stdout.write(self.style.SUCCESS(banner))
        
        os.system(f'daphne -b {host} -p {port} backend.asgi:application')
