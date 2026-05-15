<template>
<v-container fluid class="fill-height d-flex align-center justify-center" style="min-height: 100dvh;">
		<v-card class="pa-6 login-card" width="420" elevation="8" color="#f0f0f0" rounded="lg">
        
			<v-card-title class="text-h5"><svg-icon type="mdi" :path="mdiAccountPlus" /> Registro</v-card-title>
			<v-card-subtitle>Introduce tus datos para registrarte</v-card-subtitle>

			<v-card-text class="pt-4">
				<v-form>
                    <v-text-field label="Nombre" variant="outlined"/>
                    
                    <v-text-field label="Apellido" variant="outlined" />
					<v-text-field label="DNI" variant="outlined" />
                    <v-text-field label="Correo electrónico" prepend-inner-icon="mdi-email" variant="outlined" />
					<v-text-field label="Teléfono" variant="outlined" />
					<v-text-field label="Edad" variant="outlined" />
					<v-combobox
						label="Género"
						variant="outlined"
						:items="['Masculino', 'Femenino', 'Otro']"
					/>
				<v-text-field label="Usuario" prepend-inner-icon="mdi-account" variant="outlined" />
				<v-text-field
					label="Contraseña"
					prepend-inner-icon="mdi-lock"
					type="password"
					variant="outlined"
				/>
				<v-btn block color="red" size="large" class="mt-2">Registrarse</v-btn>
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