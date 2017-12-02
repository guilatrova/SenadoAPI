from rest_framework import serializers
from . import models

class LegislaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Legislatura
        fields = ('id', 'numero', 'inicio', 'fim')

class SuplenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Suplente
        fields = ('id', 'descricao_participacao', 'parlamentar_id')

class ExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exercicio
        fields = ('id', 'inicio', 'leitura', 'causa_afastamento')
        extra_kwargs = {
            'id': {'validators': []}
        }

class MandatoSerializer(serializers.ModelSerializer):
    legislaturas = LegislaturaSerializer(many=True)
    suplentes = SuplenteSerializer(many=True)
    exercicios = ExercicioSerializer(many=True)

    class Meta:
        model = models.Mandato
        fields = ('id', 'participacao', 'legislaturas', 'suplentes', 'exercicios')
        depth = 2

    def _create_inner_object(self, model, mandato, rows):
        for data in rows:
            model.objects.create(mandato=mandato, **data)

    def _create_exercicio(self, mandato, exercicios):
        for exercicio in exercicios:
            if models.Exercicio.objects.filter(id=exercicio['id']).exists():
                models.Exercicio.objects.filter(id=exercicio['id']).update(**exercicio)
            else:
                models.Exercicio.objects.create(mandato=mandato, **exercicio)

    def create(self, validated_data):
        legislaturas = validated_data.pop('legislaturas')
        suplentes = validated_data.pop('suplentes')
        exercicios = validated_data.pop('exercicios')

        mandato = models.Mandato.objects.create(**validated_data)

        self._create_inner_object(models.Legislatura, mandato, legislaturas)
        self._create_inner_object(models.Suplente, mandato, suplentes)
        self._create_exercicio(mandato, exercicios)

        return mandato

    def update(self, instance, validated_data):        
        legislaturas = validated_data.pop('legislaturas')
        suplentes = validated_data.pop('suplentes')
        exercicios = validated_data.pop('exercicios')

        instance.legislaturas.all().delete()
        instance.suplentes.all().delete()

        self._create_inner_object(models.Legislatura, instance, legislaturas)
        self._create_inner_object(models.Suplente, instance, suplentes)
        self._create_exercicio(instance, exercicios)

        models.Mandato.objects.filter(pk=validated_data['id']).update(**validated_data)

        return instance

class ParlamentarSerializer(serializers.ModelSerializer):
    mandatos = MandatoSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Parlamentar
        fields = '__all__'
        depth = 3