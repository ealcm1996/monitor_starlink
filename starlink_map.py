from flask import Flask, render_template, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, db
import os
import logging
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Obtener el directorio base de la aplicación
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Inicializar Firebase Admin
try:
    cred_dict = json.loads(os.getenv('FIREBASE_CREDENTIALS'))
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
    })
except Exception as e:
    logger.error(f"Error al inicializar Firebase: {str(e)}")
    raise

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_all_locations')
def get_all_locations():
    try:
        ref = db.reference('locations')
        locations = ref.get()
        
        if locations:
            # Imprimir los datos para debug
            print("Datos de Firebase:", locations)
            logger.debug(f"Ubicaciones obtenidas: {locations}")
            return jsonify(locations)
        else:
            logger.warning("No hay ubicaciones disponibles en Firebase")
            return jsonify({"error": "No hay ubicaciones disponibles"})
            
    except Exception as e:
        logger.error(f"Error al obtener ubicaciones: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/manifest.json')
def manifest():
    return send_from_directory(BASE_DIR, 'manifest.json')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 