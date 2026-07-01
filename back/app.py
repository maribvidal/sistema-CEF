import os
from flask import Flask
from flask_cors import CORS
from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.seed_db import insertar_datos
from routes import *
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from services.mensualidad_service import verificar_mensualidades_por_vencer, verificar_notificaciones_viejas
import subprocess
import re
import time
import tunel_state
 
load_dotenv()

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
    app.register_blueprint(mensualidad_bp)

    if not testing:
        cursor = conectarse_db()
        insertar_datos(cursor)
        cursor.connection.commit()
        cursor.connection.close()

    return app

scheduler = BackgroundScheduler()

# Ejecuta el verificar_mensualidades_por_vencer todos los días a las 9:00
scheduler.add_job(
    verificar_mensualidades_por_vencer,
    trigger="cron",
    hour=9,
    minute=0
)

# Ejecuta el verificar_notificaciones_viejas el día 1 de cada mes a las 00:00
scheduler.add_job(
    verificar_notificaciones_viejas,
    trigger="cron",
    day=1,
    hour=0,
    minute=0
)

# Esto deberia de funcionar para probar que funciona el scheduler:
# scheduler.add_job(
#     verificar_mensualidades_por_vencer,
#     trigger="interval",
#     minutes=1
# )

CLOUDFLARED = os.path.join(
    os.path.dirname(__file__),
    "tools",
    "cloudflared-windows-amd64.exe"
)

def start_tunnel(port):
    process = subprocess.Popen(
        [
            CLOUDFLARED,
            "tunnel",
            "--url",
            f"http://localhost:{port}"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    url = None

    for line in process.stdout:
        print(line.strip())

        match = re.search(r"https://[^\s]+trycloudflare\.com", line)
        if match:
            url = match.group(0)
            break

    return process, url

if __name__ == "__main__":
    app = create_app()
    scheduler.start()

    backend_proc, backend_url = start_tunnel(5000)
    frontend_proc, frontend_url = start_tunnel(5173)

    tunel_state.backend_url_state = backend_url
    tunel_state.frontend_url_state = frontend_url

    print("BACKEND:", tunel_state.backend_url_state)
    print("FRONTEND:", tunel_state.frontend_url_state)
    app.run(debug=False)
