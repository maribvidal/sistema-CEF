<template>
<v-container fluid class="fill-height d-flex align-center justify-center" style="min-height: 100dvh;">
		<v-card class="pa-6 login-card" width="420" elevation="8" color="#f0f0f0" rounded="lg">
        
			<v-card-title class="text-h5"><svg-icon type="mdi" :path="mdiAccountPlus" /> Registro</v-card-title>
			<v-card-subtitle>Introduce tus datos para registrarte</v-card-subtitle>
			<v-card-subtitle>Se debe ingresar todos los campos</v-card-subtitle>
			<v-card-text class="pt-4">
				<v-form @submit.prevent="register">
					<v-text-field v-model="dni" label="DNI" variant="outlined" />
                    <v-text-field v-model="name" label="Nombre" variant="outlined"/>
					<v-text-field v-model="lastname" label="Apellido" variant="outlined" />
					<v-text-field
					v-model="password"
					label="Contraseña"
					prepend-inner-icon="mdi-lock"
					type="password"
					variant="outlined"
					/>
					<v-text-field v-model="age" label="Fecha de nacimiento" type="date" variant="outlined" />
                    <v-text-field v-model="email" label="Correo electrónico" prepend-inner-icon="mdi-email" variant="outlined" />
					<v-text-field v-model="cellphone" label="Teléfono" variant="outlined" />
					<v-combobox
						v-model="gender"
						label="Género"
						variant="outlined"
						:items="['Masculino', 'Femenino', 'Otro']"
					/>
				<v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-3">
					{{ errorMessage }}
				</v-alert>
				<v-btn type="submit" block color="red" size="large" class="mt-2">Registrarse</v-btn>
				</v-form>
			</v-card-text>
			<v-card-text class="pt-0 mt-2" align="center">
				<v-btn to="/recuperar-contraseña" variant="flat" color="primary" size="small">
					¿Olvidaste tu contraseña?
				</v-btn>
            </v-card-text>
			<v-card-text class="pt-0 mt-2" align="center">
                <v-btn to="/inicioSesion" variant="flat" color="primary" size="small">
                    ¿Ya tienes cuenta? Inicia sesión
                </v-btn>
            </v-card-text>
		</v-card>
	</v-container>
</template>

<script setup>
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiAccountPlus } from '@mdi/js'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DateFormatterService from '@/services/DateFormatterService.js'
import { useNotificationStore } from '@/stores/notificationStore.js'

const router = useRouter()
const name = ref('')
const lastname = ref('')
const email = ref('')
/* 400: Errores lógicos de validación de inputs generales
401: El rol_id proporcionado no es válido
402: La fecha de nacimiento no cuenta con un formato válido (%Y-%m-%d)
403: El usuario debe ser mayor de 14 años
404/406: Error interno de base de datos al validar el documento
405: El DNI ya se encuentra registrado para un usuario común
407: El DNI ya se encuentra registrado para un empleado
408: Error de servidor al validar el correo electrónico
409: El correo electrónico ya se encuentra registrado
500: Error del lado del servidor al intentar insertar
200: Usuario registrado exitosamente. */

const password = ref('')
const dni = ref('')
const age = ref('')
const cellphone = ref('')
const gender = ref('')
const errorMessage = ref('')
const notificationStore = useNotificationStore()

const register = async () => {
  errorMessage.value = ''
  if (!email.value || !password.value || !name.value || !lastname.value || !age.value || !dni.value || !cellphone.value || !gender.value) {
    errorMessage.value = 'Por favor, completa todos los campos.'
    return
  }

  try {
    // El input tipo 'date' ya devuelve el valor en formato 'YYYY-MM-DD', el cual es ideal para SQLite.
    // También podemos usar DateFormatterService para asegurar consistencia si proviene de otras fuentes.
    const fechaBackend = DateFormatterService.formatDateForBackend(age.value) || age.value;

      const usuario = {
		dni: parseInt(dni.value) || 0,
		nombre: name.value,
		apellido: lastname.value,
		contraseña: password.value,
	  	fecha_nac: fechaBackend,
		correo: email.value.trim(),
		telefono: cellphone.value,
		genero: gender.value ? gender.value.charAt(0) : 'O',
      // El rol se asignará por defecto en el backend, usualmente.
        rol_id: 3
    }
	console.log("DATA ENVIADA:", usuario)

	const response = await fetch('http://127.0.0.1:5000/usuarios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(usuario),
    })

    if (!response.ok) {
	// MIRA LO QUE TE AHORRAS HERMANO. VAMOOOOOOOOOS
    //   if (response.status === 400) {
	// 	const errorData = await response.json()
	// 	errorMessage.value = errorData.message || 'Error de validación. Por favor, revisa tus datos.'
	//   } else if (response.status === 406 || response.status === 407) {
	// 	errorMessage.value = 'El correo electrónico ya se encuentra registrado.'
	//   } else if (response.status === 405) {
	// 	errorMessage.value = 'El DNI ya se encuentra registrado.'
	//   } else if (response.status === 403){
	// 	errorMessage.value = 'El usuario debe ser mayor de 14 años.'
	//   }
	// 	else {
	// 	errorMessage.value = 'Error al registrar el usuario. Por favor, intenta nuevamente.'
	//   }
		const errorData = await response.json()
	  
		// if (Array.isArray(errorData.errors)) {
		// errorMessage.value = errorData.errors
		// 	.map(err => `${err.name}: ${err.message}`)
		// 	.join('\n')
		// } else {
		errorMessage.value = errorData.message
		// 	errorData.message ||
		// 	errorData.error ||
		// 	'Error desconocido'
		// }

		return
    }

    // Si el registro es exitoso, redirigir a la página de inicio de sesión
	notificationStore.showNotification('Usuario registrado con éxito.', 'success')
    router.push({ name: 'inicioSesion' })
  } catch (error) {
    console.error('Error en el registro:', error)
    errorMessage.value = error.message
  }
}

</script>

<style scoped>
.login-card {
	width: min(420px, calc(100vw - 32px));

}
.text-h5 {
	text-align: center;
}
.v-card-subtitle {
	text-align: center;
	font-size-adjust: 0.5;
}



@media (max-width: 768px) {
	.login-card {
		width: calc(100vw - 24px);
    }
}
</style>