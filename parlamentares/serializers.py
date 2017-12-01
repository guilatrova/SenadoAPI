from rest_framework import serializers
from . import models

class ParlamentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parlamentar
        fields = '__all__'
        depth = 2

class LegislaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Legislatura
        fields = ('id', 'numero', 'inicio', 'fim')

class MandatoSerializer(serializers.ModelSerializer):
    legislaturas = LegislaturaSerializer(many=True)

    class Meta:
        model = models.Mandato
        fields = ('id', 'participacao', 'legislaturas')
        depth = 2