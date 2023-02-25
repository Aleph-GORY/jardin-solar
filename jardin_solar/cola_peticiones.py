import requests
import argparse
import os
import datetime
import time
import json

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Genera una petición a la API jardin_solar')
    args = parser.parse_args()

    timestamp = datetime.datetime.now().isoformat() + '-06:00'
    indice = os.environ['jardin_solar_endpoint'] + '/peticiones-' + os.environ['jardin_solar']
    
    try:
        while True:
            busqueda = requests.get(
                url = indice + '/_search?pretty',
                auth = (os.environ['jardin_solar_user'], os.environ['jardin_solar_pass']),
                json={
                    'query': { 'match': {
                        'estado': 'pendiente'
                    }}
                },
            )
            timestamp = datetime.datetime.now().isoformat() + '-06:00'

            for petición in busqueda.json()['hits']['hits']:
                print(petición['_source']['timestamp_peticion'], '- - Procesando petición', petición['_id'], petición['_source'])
                petición_api = requests.request(
                    method= petición['_source']['metodo'],
                    url= 'http://localhost:5000' + petición['_source']['url'],
                    data= petición['_source']['datos']
                )
                print(petición_api.status_code)
                try:
                    print(petición_api.json())
                    hay_respuesta = True
                except:
                    print('No hubo respuesta.')
                    hay_respuesta = False

                print('Actualizando petición')
                actualiza_estado = requests.post(
                    url= indice + '/_update/' + petición['_id'],
                    auth = (os.environ['jardin_solar_user'], os.environ['jardin_solar_pass']),
                    json= {
                        "script": f"ctx._source.estado = '{petición_api.status_code}'"
                    }
                )
                print('Actualiza estado', actualiza_estado.status_code)
                if hay_respuesta:
                    actualiza_respuesta = requests.post(
                        url= indice + '/_update/' + petición['_id'],
                        auth = (os.environ['jardin_solar_user'], os.environ['jardin_solar_pass']),
                        json= {
                            "script": f"ctx._source.respuesta = {json.dumps(petición_api.json()).replace('{','[').replace('}',']')}"
                        }
                    )
                    print('Actualiza respuesta', actualiza_respuesta.status_code)
                actualiza_timestamp_respuesta = requests.post(
                    url= indice + '/_update/' + petición['_id'],
                    auth = (os.environ['jardin_solar_user'], os.environ['jardin_solar_pass']),
                    json= {
                        "script": f"ctx._source.timestamp_respuesta = '{datetime.datetime.now().isoformat() + '-06:00'}'"
                    }
                )
                print('Actualiza timestamp de respuesta', actualiza_timestamp_respuesta.status_code)
                print()

            time.sleep(10)
    finally:
        print('Cola de peticiones terminada.')
