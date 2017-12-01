from rest_framework import viewsets
from .models import Parlamentar
from .serializers import ParlamentarSerializer

class ParlamentarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parlamentar.objects.all()
    serializer_class = ParlamentarSerializer