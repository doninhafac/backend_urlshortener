import os
import django
from django.utils.timezone import now
from django.core.management.base import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from links.models import ShortenedURL

class Command(BaseCommand):
    help = 'Deleta links expirados do banco de dados'

    def handle(self, *args, **kwargs):
        self.delete_expired_links()

    def delete_expired_links(self):
        expired_links = ShortenedURL.objects.filter(expires_at__lte=now())
        count = expired_links.count()
        expired_links.delete()
        self.stdout.write(f'{count} links expirados foram deletados.')
