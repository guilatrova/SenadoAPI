from django.db import models

class Parlamentar(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )

    id = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    nome_completo = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    forma_tratamento = models.CharField(max_length=15)
    foto_url = models.CharField(max_length=100)
    pagina_url = models.CharField(max_length=100)
    email = models.CharField(max_length=70, blank=True)
    sigla_partido = models.CharField(max_length=10)
    uf = models.CharField(max_length=2)
    mandato = models.OneToOneField("Mandato")

class Mandato(models.Model):
    id = models.BigIntegerField(primary_key=True)
    participacao = models.CharField(max_length=50)

class Legislatura(models.Model):
    numero = models.PositiveIntegerField()
    inicio = models.DateField()
    fim = models.DateField()
    mandato = models.ForeignKey("Mandato", related_name="legislaturas")

class Suplente(models.Model):
    descricao_participacao = models.CharField(max_length=20)
    parlamentar_id = models.BigIntegerField()
    mandato = models.ForeignKey("Mandato", related_name="suplentes")

class Exercicio(models.Model):
    id = models.BigIntegerField(primary_key=True)
    inicio = models.DateField()
    leitura = models.DateField(blank=True, null=True)
    causa_afastamento = models.CharField(max_length=100, blank=True)
    mandato = models.ForeignKey("Mandato", related_name="exercicios")