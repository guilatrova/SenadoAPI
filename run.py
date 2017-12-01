import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senadoapi.settings")
django.setup()

from parlamentares.services import SyncSenadoresEmAtividadeService

service = SyncSenadoresEmAtividadeService()
service.run()