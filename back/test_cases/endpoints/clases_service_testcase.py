from ..endpoint_test import EndpointTestCase
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.clases import insertar_clase, consultar_clase_por_id
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.instancias_clases import insertar_instancia_clase, consultar_instancia_clase_por_clase_id
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones.reservas.insertar_db import insertar_reserva

class ClasesServiceTestCase(EndpointTestCase):
    """Testcase para probar los endpoints del service de Clases."""
    def setUp(self):
        super().setUp()
        print(" > TESTING / Comenzando TestCase para el service de Clases.")

    def tearDown(self):
        super().tearDown()
        print(" > TESTING / Terminando TestCase para el service de Clases.")

    def test_listar_clases(self):
        ### ESCENARIO 2: Error en listado de clases
        res = self.client.get("/clases")

        json_res = self.decodificarRespByte(res.data)
        info = json_res["status"]

        assert info == 'error', "No habían clases cargadas y no se tiró error."
        assert '401' in str(res), "El código devuelto no es 401."

        ### ESCENARIO 1: Clases listadas con éxito
        # Crear profesores
        id_prof1 = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)["data"]
        id_prof2 = insertar_profesor("Malena", "Bancos", "F", "23234545", self.cursor)["data"]

        # Crear actividades
        id_act1 = insertar_actividad("Musculatura", 1250, self.cursor)["data"]
        id_act2 = insertar_actividad("Funcional", 1500, self.cursor)["data"]

        # Crear salas
        id_sala1 = insertar_sala("Sala 1", 10, self.cursor)["data"]
        id_sala2 = insertar_sala("Sala 2", 10, self.cursor)["data"]

        # Crear clases
        id_cla1 = insertar_clase("Activa", id_act1, id_prof1, id_sala1, "Lunes", "10:00", 10, self.cursor)["data"]
        id_cla2 = insertar_clase("Activa", id_act2, id_prof2, id_sala2, "Martes", "12:00", 5, self.cursor)["data"]

        # Crear instancia_clase
        id_ic1 = insertar_instancia_clase(id_cla1, "2026-12-02", self.cursor)["data"]
        id_ic2 = insertar_instancia_clase(id_cla2, "2026-02-02", self.cursor)["data"]

        self.cursor.connection.commit()

        # Probar endpoint "listar_clases_sin_info_extra"
        res = self.client.get("/clases")

        json_res = self.decodificarRespByte(res.data)
        json_status = json_res["status"]
        json_primera_clase = json_res["data"][0]

        assert '200' in str(res), "El código devuelto no es 200."
        assert json_status == 'success', "La respuesta no es 'success'."
        assert len(json_res["data"]) == 2, f"Se esperaban 2 clases, pero se encontraron {len(json_res['data'])}."
        assert json_primera_clase["id"] == id_cla1, f"El id de la primera clase insertada es distinto de {id_cla1}."
        assert json_primera_clase["estado"] == 'Activa', "El estado de la primera clase insertada es distinto de 'Activa'."
        assert json_primera_clase["actividad_id"] == id_act1, f"El id de la actividad de la primera clase insertada es distinto de {id_act1}."
        assert json_primera_clase["profesor_id"] == id_prof1, f"El id del profesor de la primera clase insertada es distinto de {id_prof1}."
        assert json_primera_clase["cupo_maximo"] == 10, "El cupo máximo de la primera clase insertada es distinto de 10."
        assert json_primera_clase["dia"] == 'Lunes', "La fecha es distinta a la ingresada."
        assert json_primera_clase["hora"] == '10:00', "La hora es distinta a la ingresada."
        assert json_primera_clase["sala_id"] == 1, "La sala es distinta a la ingresada."

    def test_publicar_clase(self):
        """
        ESCENARIO 1 - Clase publicada
        DADO que está en el apartado de clases, y que la sala 1 está disponible en la fecha 16/04 y horario 14:00
        CUANDO selecciona categoría yoga, sala 1, fecha 16/04, hora 14:00, y profesor Pedro, y presiona publicar clase
        ENTONCES se publica la clase en el sistema y lo redirige a la página de clases.
        """

        # Crear profesor
        id_prof = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)["data"]

        # Crear actividad
        id_act = insertar_actividad("Musculatura", 1250, self.cursor)["data"]

        # Crear sala
        id_sala = insertar_sala("Sala 1", 10, self.cursor)["data"]

        self.cursor.connection.commit()

        # Probar endpoint "publicar_clase"
        res = self.client.post("/clases", json={
            "estado": "Activa",
            "id_actividad": id_act,
            "id_profesor": id_prof,
            "id_sala": id_sala,
            "dia": "Lunes",
            "hora": "14:00",
            "cupo_maximo": 10
        })

        json_res = self.decodificarRespByte(res.data)
        json_status = json_res["status"]

        assert '200' in str(res), "El código devuelto no es 200."
        assert json_status == 'success', "La respuesta no es 'success'."

        cons_clase_creada = consultar_clase_por_id(json_res["data"], self.cursor)

        assert cons_clase_creada["data"]["dia"] == 'Lunes', "El día de la clase no coincide con el ingresado."
        
        cons_ins_clase_creada = consultar_instancia_clase_por_clase_id(json_res["data"], self.cursor)

        assert cons_ins_clase_creada["data"][0]["fecha"] == '2026-06-15', "La fecha de la instancia de la clase creada automáticamente no es correcta."

        # Revisar que se devuelve fallo por los casos donde se ponga una actividad, un profesor o una sala que no existen

        res4 = self.client.post("/clases", json={
            "estado": "Activa",
            "id_actividad": 10,
            "id_profesor": id_prof,
            "id_sala": id_sala,
            "dia": "Lunes",
            "hora": "15:00",
            "cupo_maximo": 10
        })

        assert '401' in str(res4), "El código devuelto no es 401."

        res5 = self.client.post("/clases", json={
            "estado": "Activa",
            "id_actividad": id_act,
            "id_profesor": 10,
            "id_sala": id_sala,
            "dia": "Lunes",
            "hora": "15:00",
            "cupo_maximo": 10
        })

        assert '403' in str(res5), "El código devuelto no es 403."

        res6 = self.client.post("/clases", json={
            "estado": "Activa",
            "id_actividad": id_act,
            "id_profesor": id_prof,
            "id_sala": 10,
            "dia": "Lunes",
            "hora": "15:00",
            "cupo_maximo": 10
        })

        assert '405' in str(res6), "El código devuelto no es 405."

        """
        ESCENARIO 2: Sala ocupada
        DADO que está en el apartado de clases y que la sala 1 no está disponible el día Lunes en el horario 14:00
        CUANDO selecciona estado “Activa”, id de actividad 1, id de profesor 1, sala 1, dia “Lunes”, hora 14:00, cupo máximo 10, y presiona publicar clase
        ENTONCES el sistema informa que ya hay una clase en esa sala en ese horario
        """

        res2 = self.client.post("/clases", json={
            "estado": "Activa",
            "id_actividad": id_act,
            "id_profesor": id_prof,
            "id_sala": id_sala,
            "dia": "Lunes",
            "hora": "14:00",
            "cupo_maximo": 10
        })

        json_res2 = self.decodificarRespByte(res2.data)
        json_status2 = json_res2["status"]

        assert '407' in str(res2), "El código devuelto no es 407."
        assert json_status2 == 'error', "La respuesta no es 'error'."

        """
        ESCENARIO 3: Fallo por cupo máximo que supera la capacidad de la sala
        DADO que está en el apartado de clases, y que la sala 2 está disponible el día Lunes en el horario 14:00, y la sala 2 tiene una capacidad de 8 personas.
        CUANDO selecciona estado “Activa”, id de actividad 1, id de profesor 1, sala 2, dia “Lunes”, hora 14:00, cupo máximo 10, y presiona publicar clase
        ENTONCES el sistema informa que la clase no se pudo publicar debido a que el cupo máximo elegido supera la capacidad que tiene la sala.
        """

        id_sala2 = insertar_sala("Sala 2", 8, self.cursor)["data"]

        self.cursor.connection.commit()

        res3 = self.client.post("/clases", json={
            "estado": "Activa",
            "id_actividad": id_act,
            "id_profesor": id_prof,
            "id_sala": id_sala2,
            "dia": "Lunes",
            "hora": "14:00",
            "cupo_maximo": 10
        })

        json_res3 = self.decodificarRespByte(res3.data)
        json_status3 = json_res3["status"]

        assert '408' in str(res3), "El código devuelto no es 408."
        assert json_status3 == 'error', "La respuesta no es 'error'."

        # Faltan cubrir dos códigos de error

    def test_reservar_clase(self):
        """
        ESCENARIO 1: Reserva exitosa
        Dado el cliente con dni "41298622” que cuenta con la sesión activada, la clase pertenezca al rango de fechas que cubre la mensualidad, la clase “Pilates” 
            con cupos disponibles y no cuenta con otra actividad dentro del rango horario de las 18:00hs.
        Cuando el cliente con dni “41298622” seleccione la actividad “Pilates”, horario 18:00hs y presione “Confirmar reserva”.
        Entonces el sistema registra la reserva, resta un cupo de la clase, Informa operación exitosa
        """

        # Crear rol, cliente, actividad, profesor, sala, clase, instancia_clase
        id_cli = insertar_usuario("41298622", "Mariano", "Venal", "12345678", "2004-02-02", "marianovenal@gmail.com", "542215253779", "M", 1, self.cursor)["data"]
        id_prof = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)["data"]
        id_act = insertar_actividad("Pilates", 1250, self.cursor)["data"]
        id_sala = insertar_sala("Sala 2", 10, self.cursor)["data"]
        id_cla = insertar_clase("Activa", id_act, id_prof, id_sala, "Lunes", "18:00", 10, self.cursor)["data"]
        id_ic = insertar_instancia_clase(id_cla, "2026-12-02", self.cursor)["data"]

        self.cursor.connection.commit()

        # Probar endpoint "reservar_clase" 
        res = self.client.put(f"/clases/{id_ic}/reservar", json={
            "id_usuario": id_cli
        })

        json_res = self.decodificarRespByte(res.data)

        assert '200' in str(res), "El código devuelto no es 200."
        assert json_res["status"] == 'success', "La respuesta devolvió 'success'."
        assert json_res["data"] == 1, "Se insertó una nueva reserva."
    
        """
        ESCENARIO 4: Reserva fallida por superposición de horarios  
        Dado el cliente con dni "41298622" con sesión iniciada, la clase pertenece al rango de fechas que cubre la mensualidad, la clase “Pilates” 
            no se encuentra llena y tiene la clase reservada de “Yoga” a las 18:00hs.     
        Cuando el cliente con dni "41298622" seleccione la clase “Pilates”, horario "18:00hs" presione “Confirmar Reserva”     
        Entonces el sistema informa “El usuario ya se encuentra inscripto en una clase que ocurre ese día a esa hora.”
        """

        id_act2 = insertar_actividad("Yoga", 1500, self.cursor)["data"]
        id_prof2 = insertar_profesor("Lisa", "Bruselas", "F", "44442222", self.cursor)["data"]
        id_cla2 = insertar_clase("Activa", id_act2, id_prof2, id_sala, "Lunes", "18:00", 10, self.cursor)["data"]
        id_ic2 = insertar_instancia_clase(id_cla2, "2026-12-02", self.cursor)["data"]

        self.cursor.connection.commit()

        # Probar endpoint "reservar_clase" 
        res = self.client.put(f"/clases/{id_ic2}/reservar", json={
            "id_usuario": id_cli
        })

        json_res = self.decodificarRespByte(res.data)

        assert '405' in str(res), "El código devuelto no es 405."
        assert json_res["status"] == 'error', "La respuesta devolvió 'error'."
        
        """
        ESCENARIO 3: Reserva fallida por falta de cupo
        Dado el cliente con dni “98292612” con sesión iniciada, la clase pertenece al rango de fechas que cubre la mensualidad, y la clase “Yoga” se encuentra llena. 
        Cuando el cliente con dni “98292612” seleccione la clase “Yoga”, horario 19:00hs y presione “Confirmar reserva”
        Entonces el sistema informa que no hay cupos y le ofrece la opción de "Inscribirse en lista de espera".
        """

        id_cla3 = insertar_clase("Activa", id_act2, id_prof2, id_sala, "Lunes", "19:00", 5, self.cursor)["data"]
        id_ic3 = insertar_instancia_clase(id_cla3, "2026-12-02", self.cursor)["data"]
        for i in range(0, 5):
            id_cli_nuevo = insertar_usuario(f"40123412{i}", "Cliente", f"N°{i}", "12345678", "2004-02-02", f"cli{i}@gmail.com", "542215253779", "M", 1, self.cursor)["data"]
            insertar_reserva(id_cli_nuevo, id_ic3, self.cursor)
        
        self.cursor.connection.commit()

        # Probar endpoint "reservar_clase" 
        res = self.client.put(f"/clases/{id_ic3}/reservar", json={
            "id_usuario": id_cli
        })

        json_res = self.decodificarRespByte(res.data)

        assert '406' in str(res), "El código devuelto no es 406."
        assert json_res["status"] == 'error', "La respuesta devolvió 'error'."

    def test_verificar_inscripcion_usuario_clase(self):
        id_cli = insertar_usuario("41298622", "Mariano", "Venal", "12345678", "2004-02-02", "marianovenal@gmail.com", "542215253779", "M", 1, self.cursor)["data"]
        id_prof = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)["data"]
        id_act = insertar_actividad("Pilates", 1250, self.cursor)["data"]
        id_sala = insertar_sala("Sala 2", 10, self.cursor)["data"]
        id_cla = insertar_clase("Activa", id_act, id_prof, id_sala, "Lunes", "18:00", 10, self.cursor)["data"]
        id_ic = insertar_instancia_clase(id_cla, "2026-12-02", self.cursor)["data"]
        id_re = insertar_reserva(id_cli, id_ic, self.cursor)["data"]

        # Probar endpoint "verificar_inscripcion_usuario_clase"
        res = self.client.get(f"/clases/{id_ic}/verificar", json={
            "id_usuario": id_cli
        })

        json_res = self.decodificarRespByte(res.data)

        assert json_res["status"] == 'success', "La respuesta del endpoint no fue un 'success'."
