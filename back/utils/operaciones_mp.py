from os import getenv

import requests

Access_Token = getenv("Access_Token")

external_codes = {
    "mensualidad": "MENSUALIDAD",
    "clase_particular": "CLASE-PARTICULAR"
}

def getExternalCode(nombre, id):
    return external_codes[nombre] + "-" + str(id)

# puse valores randoms
items= {
  "mensualidad": {
    "title": "Mensualidad",
    "unit_price": 10000.00,
    "quantity": 1,
    "unit_measure": "unit",
    "external_categories": [
      {"id": "gym-membership"}
    ]
  },
  "clase_particular": {
    "title": "Clase particular",
    "unit_price": 2000.00,
    "quantity": 1,
    "unit_measure": "unit",
    "external_categories": [
      {"id": "personal-training"}
    ]
  }
}

def getItem(nombre, id):
    if nombre in items:
        item = items[nombre]
        item["external_code"] = getExternalCode(nombre, id)
        return item
    return None

# esto habria que agregarlo cualquier cosa para los descuentos
discounts = {
    "payment_methods": [
        {
            "new_total_amount": "47.28",
            "type": "account_money"
        }
    ]
}

# External_reference:
# 	Es la referencia externa de la order, asignada al momento de la creación. El límite máximo permitido es de 64 caracteres y los permitidos son: letras mayúsculas y minúsculas,
# números y los símbolos guion (-) y guion bajo (_). El campo no puede utilizarse para enviar datos PII. Además, este valor debe ser único para cada order, 
# ya que actúa como el identificador de dicha order

# Descripcion:
# Descripción del producto o servicio. El límite máximo es de 150 caracteres y no puede utilizarse para enviar datos PII. (en el ejemplo pone Smartphone)

# Total_amount:
# Valor total de la order. Representa la suma de las transacciones. Puede contener dos decimales o ninguno. Ejemplo: 50.00.

# el modo puede ser:
# Modelo estático: En este modelo, un único código QR asociado a la caja creada previamente recibe la información de cada order generada.
# Modelo dinámico: Un código QR exclusivo y de pago único es generado para cada transacción, conteniendo los datos específicos de la order creada.
# Modelo híbrido: Permite que el pago se realice tanto por el QR estático como por el dinámico. La order se vincula al código QR estático de la caja, mientras que también se genera un QR dinámico simultáneamente. Una vez que se realice el pago con cualquiera de los dos códigos, el otro quedará automáticamente inhabilitado para su uso.

# en el modo estatico (que es el que implemento), el qr que se manda es el que esta en el la imagen del .env

# respuesta tipo:
# {
#    "id": "ORD01K371WBFDS4MD9JG0K8ZMECBE",
#    "type": "qr",
#    "processing_mode": "automatic",
#    "external_reference": "ext_ref_1234",
#    "description": "Smartphone",
#    "total_amount": "50.00",
#    "expiration_time": "PT16M",
#    "country_code": "ARG",
#    "user_id": "{{USER_ID}}",
#    "status": "created",
#    "status_detail": "created",
#    "currency": "ARS",
#    "created_date": "2025-08-21T19:32:21.621Z",
#    "last_updated_date": "2025-08-21T19:32:21.621Z",
#    "integration_data": {
#        "application_id": "{{APPLICATION_ID}}"
#    },
#    "transactions": {
#        "payments": [
#            {
#                "id": "PAY01K371WBFDS4MD9JG0KCV6PRKQ",
#                "amount": "50.00",
#                "status": "created",
#                "status_detail": "ready_to_process"
#            }
#        ]
#    },
#    "config": {
#        "qr": {
#            "external_pos_id": "STORE001POS001",
#            "mode": "static"
#        }
#    },
#    "items": [
#        {
#            "title": "Smartphone",
#            "unit_price": "50.00",
#            "unit_measure": "kg",
#            "external_code": "777489134",
#            "quantity": 1,
#            "external_categories": [
#                {
#                    "id": "device"
#                }
#            ]
#        }
#    ],
#    "discounts": {
#        "payment_methods": [
#            {
#                "type": "account_money",
#                "new_total_amount": "47.28"
#            }
#        ]
#    }
# }

# idea: crear un pago antes de generar el orden con estado "pending" y obtenes su id, pasas el id como external reference
# luego actualizas el estado del pago segun la consulta de la orden, cualquier cosa se elimina el pago si hay algun fallo
def crear_orden_qr_mp(external_reference, total_amount, description, datos_item):
    url = 'https://api.mercadopago.com/v1/orders'
    headers = {'Authorization': f'Bearer {Access_Token}'}

    respuesta = requests.post(url, headers=headers)

    if "nombre" not in datos_item or "id" not in datos_item:
        return {
            "status": "error",
            "message": "Datos del item incompletos. Se requiere 'nombre' e 'id'."
        }
        
    if datos_item["id"] is None:
        return {
            "status": "error",
            "message": "El ID del item es requerido."
        }

    item = getItem(datos_item["nombre"], datos_item["id"])

    if item is None:
        return {
            "status": "error",
            "message": f"Item con nombre '{datos_item['nombre']}' no encontrado."
        }

    datos = {
        "type": "qr",
        "total_amount": total_amount,
        "description": description,
        "external_reference": external_reference,
        "expiration_time": "PT16M",
        "config": {
            "qr": {
                "external_pos_id": "CAJA001",
                "mode": "static"
            }
        },
        "transactions": {
            "payments": [
                {
                "amount": total_amount
                }
            ]
        },
        "items": [
            item
        ]
    }
    respuesta = requests.post(url, json=datos, headers=headers)

    print(respuesta.json())
    
    return respuesta.json()

# el id de la orden se obtiene en la respuesta de la creacion de la orden

# respuesta tipo:
# {
#    "id": "ORD01K371WBFDS4MD9JG0K8ZMECBE",
#    "type": "qr",
#    "processing_mode": "automatic",
#    "external_reference": "ext_ref_1234",
#    "description": "Smartphone",
#    "total_amount": "50.00",
#    "expiration_time": "PT16M",
#    "country_code": "ARG",
#    "user_id": "{{USER_ID}}",
#    "status": "canceled",
#    "status_detail": "canceled",
#    "currency": "ARS",
#    "created_date": "2025-08-21T19:32:21.621Z",
#    "last_updated_date": "2025-08-21T19:33:52.012Z",
#    "integration_data": {
#        "application_id": "{{APPLICATION_ID}}"
#    },
#    "transactions": {
#        "payments": [
#            {
#                "id": "PAY01K371WBFDS4MD9JG0K8ZMECBE",
#                "amount": "50.00",
#                "status": "canceled",
#                "status_detail": "canceled_by_api"
#            }
#        ]
#    },
#    "config": {
#        "qr": {
#            "external_pos_id": "STORE001POS001",
#            "mode": "static"
#        }
#    },
#    "items": [
#        {
#            "title": "Smartphone",
#            "unit_price": "50.00",
#            "unit_measure": "kg",
#            "external_code": "777489134",
#            "quantity": 1,
#            "external_categories": [
#                {
#                    "id": "device"
#                }
#            ]
#        }
#    ],
#    "discounts": {
#        "payment_methods": [
#            {
#                "type": "account_money",
#                "new_total_amount": "47.28"
#            }
#        ]
#    }
# }

# esto no se utilizaria, de todas formas lo dejo por las dudas pero se notifica con webhooks y el front es el que hace el loop y pregunta al back por el estado del pago
def consultar_datos_orden_qr_mp(id_orden):
    url = f'https://api.mercadopago.com/v1/orders/{id_orden}'
    headers = {'Authorization': f'Bearer {Access_Token}'}
    respuesta = requests.get(url, headers=headers)
    return respuesta.json()

# mirar posibles estados del order para despues controlarlo.

# creacion de cajas y sucursales. solo se ejecuta una vez.
def crear_caja_mp():
    url = 'https://api.mercadopago.com/pos'
    headers = {'Authorization': f'Bearer {Access_Token}'}

    # Para una petición GET
    respuesta = requests.post(url, headers=headers)

    # Para una petición POST con JSON
    datos = {
    "name": "First POS",
    "fixed_amount": True,
    "store_id": 83558234,
    "external_store_id": "sucursal-la-plata-001",
    "external_id": "CAJA001"
    }

    respuesta = requests.post(url, json=datos, headers=headers)

    print(respuesta.json())
    
def crear_sucursal_mp():
    usr_id = getenv("User_ID")

    url = f'https://api.mercadopago.com/users/{usr_id}/stores'
    headers = {'Authorization': f'Bearer {Access_Token}'}

    # Para una petición GET
    respuesta = requests.post(url, headers=headers)

    # Para una petición POST con JSON
    datos = {
    "name": "Sucursal Instore",
    "business_hours": {
        "monday": [
        {
            "open": "08:00",
            "close": "17:00"
        }
        ],
        "tuesday": [
        {
            "open": "08:00",
            "close": "17:00"
        }
        ],
        "wednesday": [
        {
            "open": "08:00",
            "close": "17:00"
        }
        ],
        "thursday": [
        {
            "open": "08:00",
            "close": "17:00"
        }
        ],
        "friday": [
        {
            "open": "08:00",
            "close": "17:00"
        }
        ],
        "saturday": [
        {
            "open": "08:00",
            "close": "12:00"
        }
        ],
        "sunday": [
        {
            "open": "08:00",
            "close": "12:00"
        }
        ]
    },
    "external_id": "sucursal-la-plata-001",
    "location": {
        "street_number": "742",
        "street_name": "Calle 12",
        "city_name": "La Plata",
        "state_name": "Buenos Aires",
        "latitude": -34.92145,
        "longitude": -57.95453,
        "reference": "Zona céntrica de La Plata, cerca de Plaza Moreno."
    }
    }

    respuesta = requests.post(url, json=datos, headers=headers)

    print(respuesta.json())