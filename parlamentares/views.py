from rest_framework import viewsets
from .models import Parlamentar, Mandato
from .serializers import ParlamentarSerializer, MandatoSerializer

class ParlamentarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parlamentar.objects.all()
    serializer_class = ParlamentarSerializer

class MandatoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mandato.objects.all()
    serializer_class = MandatoSerializer