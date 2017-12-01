import requests
from . import models
from .serializers import ParlamentarSerializer, MandatoSerializer

URL = "http://legis.senado.gov.br/dadosabertos/senador/lista/atual"
HEADERS = {'Accept': 'application/json'}

class SyncSenadoresEmAtividadeService:
    def __init__(self):
        self.headers = {}

    def run(self):
        response = requests.get(URL, headers=HEADERS)
        if response.ok:
            data = response.json().get('ListaParlamentarEmExercicio').pop('Parlamentares').pop('Parlamentar')
            self._sync(data)
        else:
            raise Exception(response.json())

    def _sync(self, data):
        for parlamentar_root in data:
            try:
                data = self._map_mandato(parlamentar_root['Mandato'])
                mandato = self._get_or_create(
                    data, 
                    models.Mandato,
                    MandatoSerializer
                )

                data = self._map_parlamentar(parlamentar_root['IdentificacaoParlamentar'])
                parlamentar = self._get_or_create(
                    data,
                    models.Parlamentar,
                    ParlamentarSerializer,
                    mandato=mandato
                )
                print('ok')
            except Exception as excp:
                print(excp)

    def _get_or_create(self, data, entity, serializer_cls, **kwargs):
        instance = None
        if entity.objects.filter(id=data['id']).exists():
            instance = entity.objects.get(id=data['id'])

        serializer = serializer_cls(instance, data=data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save(**kwargs)
        return saved

    def _map_parlamentar(self, raw):
        return {
            'id': raw['CodigoParlamentar'],
            'nome': raw['NomeParlamentar'],
            'nome_completo': raw['NomeCompletoParlamentar'],
            'sexo': self._map_sexo(raw['SexoParlamentar']),
            'forma_tratamento': raw['FormaTratamento'],
            'foto_url': raw['UrlFotoParlamentar'],
            'pagina_url': raw['UrlPaginaParlamentar'],
            'email': raw.get('EmailParlamentar', ''),
            'sigla_partido': raw['SiglaPartidoParlamentar'],
            'uf': raw['UfParlamentar']
        }

    def _map_sexo(self, sexo):
        return 'M' if sexo == 'Masculino' else 'F'

    def _map_mandato(self, raw):
        return {
            'id': raw['CodigoMandato'],
            'participacao': raw['DescricaoParticipacao'],
            'legislaturas': self._map_legislaturas(raw),
            'suplentes': self._map_suplentes(raw['Suplentes']['Suplente']),
            'exercicios': self._map_exercicios(raw['Exercicios']['Exercicio'])
        }

    def _map_legislaturas(self, raw):
        return [
            self._map_legislatura(raw['PrimeiraLegislaturaDoMandato']),
            self._map_legislatura(raw['SegundaLegislaturaDoMandato'])
        ]

    def _map_legislatura(self, raw):
        return {
            'numero': raw['NumeroLegislatura'],
            'inicio': raw['DataInicio'],
            'fim': raw['DataFim']
        }

    def _map_suplentes(self, raw):
        if isinstance(raw, list):
            return [self._map_suplente(x) for x in raw]
        else:
            return [self._map_suplente(raw)]
        

    def _map_suplente(self, raw):
        return {
            'descricao_participacao': raw['DescricaoParticipacao'],
            'parlamentar_id': raw['CodigoParlamentar']            
        }

    def _map_exercicios(self, raw):
        if isinstance(raw, list):
            return [self._map_exercicio(x) for x in raw]
        else:
            return [self._map_exercicio(raw)]

    def _map_exercicio(self, raw):
        return {
            'id': raw['CodigoExercicio'],
            'inicio': raw['DataInicio'],
            'leitura': raw.get('DataLeitura', None),
            'causa_afastamento': raw.get('DescricaoCausaAfastamento', '')
        }