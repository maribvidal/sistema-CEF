<template>
	<v-container class="fill-height d-flex align-center justify-center">
		<v-card class="pa-6" width="420" elevation="8" color="#f0f0f0" rounded="lg">
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
				<v-form>
					<v-text-field label="Usuario" prepend-inner-icon="mdi-account" variant="outlined" />
					<v-text-field
						label="Contraseña"
						prepend-inner-icon="mdi-lock"
						type="password"
						variant="outlined"
					/>
					<v-btn block color="red" size="large" class="mt-2">Entrar</v-btn>
				</v-form>
			</v-card-text>
            <v-card-text class ="pt-0 mt-2" align="center">
                <v-btn text color="primary" size="small">¿Olvidaste tu contraseña?</v-btn>
            </v-card-text>
		</v-card>
	</v-container>
</template>

<script setup>
import logoImg from '@/assets/logoLargo.png'
</script>

