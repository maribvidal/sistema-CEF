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
        rol: 3
    }

	const response = await fetch('http://127.0.0.1:5000/usuarios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(usuario),
    })

    if (!response.ok) {
      const errorData = await response.text()
      throw new Error(errorData || 'Error al registrar el usuario.')
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