# Senado API

Projeto responsável por sincronizar dados dos senadores em atividade e disponbilizar através de uma API.

Os dados são recuperados através do seguinte endpoint: http://legis.senado.gov.br/dadosabertos/senador/lista/atual .

Os dados armazenados no banco da aplicação são informações dos senadores e mandatos.

## API

Os dados sincronizados são expostos pelos seguintes endpoints:

| Endpoint | Resultado |
|---|---|
| `/api/parlamentares` | Lista com todos os parlamentares |
| `/api/parlamentares/:id` | Detalhes sobre o parlamentar definido |
| `/api/mandatos` | Lista com todos os mandatos, incluindo legislaturas, suplentes e exercícios |
| `/api/mandatos/:id` | Detalhes sobre o mandado definido, incluindo legislaturas, suplentes e exercícios |

## Sincronizar

Para sincronizar os dados da aplicação com o webservice do senado, basta executar:

`python sync_api.py` , e será efetuado criação ou atualização das informações.

Desta forma é possível configurar como um job e rodar todo(a) hora, dia, semana, mês. Também é simples o bastante para ser invocado pela própria aplicação.

> ***Obs:** Lembrar de instalar as dependências antes de rodar esse comando, explicado em detalhes abaixo. A sincronização utiliza os serializers do **Django Rest Framework**.*

## Instalando e executando o app (Windows)

```
git clone https://github.com/guilatrova/SenadoAPI.git
cd SenadoAPI
virtualenv venv
venv\scripts\activate
pip install -r requirements.txt

python manage.py migrate
python sync_api.py
python manage.py runserver
```

Agora você pode acessar http://localhost:8000/api/mandatos/ e deve ver uma lista com todos os mandatos :)