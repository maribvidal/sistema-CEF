from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from flask import Flask
from flask_cors import CORS
from routes import *
from test_cases import test_consultar_esqueleto, test_insertar_datos, test_login_service
from db.operaciones.seed_db import insertar_datos
from test_cases.test_consultar_esqueleto import intentar_consultar_esqueleto

# --- INICIALIZAR BD ---
reconstruir_db()

# --- INICIALIZAR APP FLASK ---
app = Flask(__name__)
CORS(app)

# --- INICIALIZAR BLUEPRINTS DE FLASK ---
app.register_blueprint(usuario_bp)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(clases_bp)
app.register_blueprint(empleados_bp)
app.register_blueprint(pagos_bp)

# --- REALIZAR TESTS ---
cursor = conectarse_db()

insertar_datos(cursor)
intentar_consultar_esqueleto(cursor)

#test_insertar_datos.intentar_insertar_datos(cursor)
#test_consultar_esqueleto.intentar_consultar_esqueleto()
#test_login_service.intentar_login_service()

cursor.connection.close()

if __name__ == "__main__":
    app.run(debug=True)
