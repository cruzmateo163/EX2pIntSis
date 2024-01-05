from flask import Flask, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
''''app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@host/el_mundo_en_tus_manos'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@127.0.0.1/el_mundo_en_tus_manos'

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    ciudad_residencia = db.Column(db.String(120), nullable=False)

''''@app.route('/datos/<nombre_usuario>', methods=['GET'])
def obtener_georreferenciacion(nombre_usuario):
    cliente = Cliente.query.filter_by(nombre_usuario=nombre_usuario).first()
    if cliente:
        # Aquí llamarías a la función para obtener los datos de georreferenciación
        # Puedes usar la API de Geocode.xyz como se mostró anteriormente
        # En este ejemplo, simplemente retornamos la ciudad de residencia
        return jsonify({'ciudad_residencia': cliente.ciudad_residencia})
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

if __name__ == '__main__':
    app.run(port=8290, debug=True)'''


GEODATA_API_URL = "https://geocode.xyz/{}?json=1"  # URL base de la API

@app.route('/datos/<nombre_usuario>', methods=['GET'])
def obtener_georreferenciacion(nombre_usuario):
    cliente = Cliente.query.filter_by(nombre_usuario=nombre_usuario).first()

    if cliente:
        # Llamar a la función para obtener datos de georreferenciación
        datos_georreferenciacion = obtener_datos_georreferenciacion(cliente.ciudad_residencia)
        return jsonify(datos_georreferenciacion)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

def obtener_datos_georreferenciacion(ciudad_residencia):
    # Construir la URL completa de la API de Geocode.xyz
    api_url = GEODATA_API_URL.format(ciudad_residencia)

    try:
        # Realizar la solicitud a la API de Geocode.xyz
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción para errores HTTP

        # Analizar la respuesta JSON
        datos_georreferenciacion = response.json()

        return datos_georreferenciacion

    except requests.RequestException as e:
        # Manejar cualquier error de solicitud
        return jsonify({'error': f'Error al llamar a la API: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=8290, debug=True)