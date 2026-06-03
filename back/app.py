import os
from flask import Flask
from flask_cors import CORS
from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.seed_db import insertar_datos
from routes import *

from test_cases.test_consultar_esqueleto import intentar_consultar_esqueleto

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

    if not app.testing:
        cursor = conectarse_db()
        insertar_datos(cursor)
        cursor.connection.close()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
