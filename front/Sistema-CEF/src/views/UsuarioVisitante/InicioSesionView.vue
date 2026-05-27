<template>
	<v-container fluid class="fill-height d-flex align-center justify-center" style="min-height: 100dvh;">
		<v-card class="pa-6 login-card" width="420" elevation="8" color="#f0f0f0" rounded="lg">
            <v-img
                :src="logoImg"
                alt="Logo CEF"
                contain
                height="100"
                class="mb-4"
            />
			<v-card-title class="text-h5">Inicio de sesión</v-card-title>
			<v-card-subtitle>Accede al sistema con tus credenciales</v-card-subtitle>

			<v-card-text class="pt-4">
				<v-form @submit.prevent="login">
					<v-text-field v-model="email" label="E-Mail" prepend-inner-icon="mdi-account" variant="outlined" />
					<v-text-field
						v-model="password"
						label="Contraseña"
						prepend-inner-icon="mdi-lock"
						type="password"
						variant="outlined"
					/>
					<v-btn block color="red" size="large" class="mt-2" type="submit">Entrar</v-btn>
					<v-alert v-if="errorMessage" type="error" class="mt-2">
						{{ errorMessage }}
					</v-alert>
				</v-form>
			</v-card-text>
			<v-card-text class="pt-0 mt-2" align="center">
				<v-btn to="/recuperar-contraseña" variant="flat" color="primary" size="small">
					¿Olvidaste tu contraseña?
				</v-btn>
            </v-card-text>
			<v-card-text class="pt-0 mt-2" align="center">
				<v-btn to="/registro" variant="flat" color="primary" size="small">
					¿No tienes cuenta? Regístrate
				</v-btn>
            </v-card-text>
		</v-card>
	</v-container>
</template>

<script setup>
import logoImg from '@/assets/logoLargo.png'
import { useAuth } from '@/services/UsuariosServices.js'
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useNotificationStore } from '@/stores/notificationStore.js'

const { login: authLogin } = useAuth()
const notificationStore = useNotificationStore()
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const login = async () => {
	errorMessage.value = ''
	try {
		const userInfo = await authLogin({
			email: email.value,
			password: password.value,
		})
		if (userInfo) {
			notificationStore.showNotification('Usuario iniciado sesión con éxito, Bienvenido ' + userInfo.nombre + '.', 'success')
			router.push('/')
		}
	} catch (error) {
		console.error('Error en el inicio de sesión:', error)
		const status = error?.response?.status || error?.status
		if (status === 400) {
			errorMessage.value = 'Usuario no registrado'
		} else if (status === 401) {
			errorMessage.value = 'Contraseña incorrecta'
		} else {
			errorMessage.value = error?.message || 'Ocurrió un error al iniciar sesión'
		}
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
