import requests
import argparse
import os
import datetime

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Genera una petición a la API jardin_solar')
    parser.add_argument('jardin', help='Identificador único del Jardín.')
    parser.add_argument('metodo', help='Método HTTP en la petición.')
    parser.add_argument('url', help='Ruta a la API jardin_solar.')
    parser.add_argument('-d', '--datos', help='Cuerpo de la petición.')
    args = parser.parse_args()

    indice = os.environ['jardin_solar_endpoint'] + '/peticiones-' + args.jardin + '/_doc?pretty'
    petición = {
        'metodo': args.metodo,
        'url': args.url,
        'datos': args.datos,
        'estatus': 'esperando',
        'timestamp_peticion': datetime.datetime.now().isoformat() + "-06:00",
    }
    
    peticion_db = requests.post(
        url = indice, 
        auth = (os.environ['jardin_solar_user'], os.environ['jardin_solar_pass']),
        json = petición
    )

    print(peticion_db.json())