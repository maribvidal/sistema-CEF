import os
from flask import Flask
from flask_cors import CORS
from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.seed_db import insertar_datos
from routes import *
import ngrok
from dotenv import load_dotenv
 
load_dotenv()

def connect_ngrok():
    forwarder = ngrok.forward("localhost:5000", authtoken_from_env=True)
    print(f"Available at: {forwarder.url()}")

def create_app(testing=False, db_name="database.db"):
    
    os.environ["NOM_DB"] = db_name

    if not testing:
        reconstruir_db()

    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = testing
    
    CORS(app)

    app.register_blueprint(usuario_bp)
    app.register_blueprint(autenticacion_bp)
    app.register_blueprint(clases_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(salas_bp)
    app.register_blueprint(actividades_bp)
    app.register_blueprint(profesores_bp)
    app.register_blueprint(empleados_bp)
    app.register_blueprint(permisos_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(metricas_bp)
    app.register_blueprint(notificaciones_bp)
    app.register_blueprint(mensualidad_bp)

    if not app.testing:
        cursor = conectarse_db()
        insertar_datos(cursor)
        cursor.connection.close()

    return app

# puse el debug en false porq me tiraba error el ngrok
if __name__ == "__main__":
    app = create_app()
    connect_ngrok()
    app.run(debug=False)
