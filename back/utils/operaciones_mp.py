import requests

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
def crear_orden_qr_mp(external_reference, total_amount, description):
    url = 'https://api.mercadopago.com/v1/orders'
    headers = {'Authorization': 'Bearer APP_USR-786188901526033-061219-7f8ea4f40999726883d4f645034a3020-3470890874'}

    respuesta = requests.post(url, headers=headers)


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
        "amount": "50.00"
        }
    ]
    },
    "items": [
    {
        "title": "Smartphone",
        "unit_price": "50.00",
        "quantity": 1,
        "unit_measure": "kg",
        "external_code": "777489134",
        "external_categories": [
        {
            "id": "device"
        }
        ]
    }
    ],
    "discounts": {
    "payment_methods": [
        {
        "new_total_amount": "47.28",
        "type": "account_money"

        }
        ]
    }
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
def consultar_datos_orden_qr_mp(id_orden):
    url = f'https://api.mercadopago.com/v1/orders/{id_orden}'
    headers = {'Authorization': 'Bearer APP_USR-786188901526033-061219-7f8ea4f40999726883d4f645034a3020-3470890874'}
    respuesta = requests.get(url, headers=headers)
    return respuesta.json()

# mirar posibles estados del order para despues controlarlo.