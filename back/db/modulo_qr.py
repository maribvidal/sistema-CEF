import io
import qrcode

def generar_qr(id_cliente: int):
    buffer = io.BytesIO()

    img = qrcode.make(str(id_cliente))
    img.save(buffer, format="PNG")

    buffer.seek(0)

    return buffer

# Los del back no se encargarían de escanear el QR, sino que de generarlo y validar si, efectivamente, ese usuario posee una reserva para la instancia de clase actual.
# QR
#  ↓
# Contiene: 8201
#  ↓
# Frontend lo escanea
#  ↓
# POST /asistencias/validar (es un ejemplo, no se si se llama así)
# {
#     "id_cliente": 8201
# }
