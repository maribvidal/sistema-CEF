<template>
  <v-container class="metrics-container" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" md="6">

        <!-- Selector de métrica -->
        <v-btn-toggle v-model="metricaSeleccionada" mandatory class="mb-4" rounded="lg">
          <v-btn value="plataRecaudada">Plata recaudada</v-btn>
          <v-btn value="clasesCanceladas">Clases canceladas</v-btn>
          <v-btn value="clasesConMensualidad">Clases con mensualidad</v-btn>
        </v-btn-toggle>
              <div v-if="mostrarFiltroFecha" class="d-flex align-center gap-2 mb-4">
        <v-text-field
          v-model="fechaInicio"
          label="Fecha inicio"
          type="date"
          density="compact"
          hide-details
        />
        <v-text-field
          v-model="fechaFin"
          label="Fecha fin"
          type="date"
          density="compact"
          hide-details
        />
        <v-btn @click="cargarConFiltro" :disabled="!fechaInicio || !fechaFin">
          Filtrar
        </v-btn>
        <v-btn variant="text" @click="limpiarFiltro">Limpiar</v-btn>
      </div>

        <!-- Mostrar mensaje si no hay datos -->
        <div v-if="metricaActual.datos.labels.length === 0" class="text-center my-4">
          <v-icon size="48" color="grey lighten-1">mdi-database-off</v-icon>
          <p class="text-subtitle-1 mt-2">No hay datos disponibles para la métrica seleccionada.</p>
        </div>

        <!-- Card única que cambia según la selección -->
        <v-card class="pa-4" elevation="2">
          <v-card-title class="text-h5">{{ metricaActual.titulo }}</v-card-title>
          <v-card-subtitle>{{ metricaActual.subtitulo }}</v-card-subtitle>
          <!-- si se selecciona una fecha, mostrarla -->
          
          <v-card-text>
            <BarChart :chartData="metricaActual.datos" />
          </v-card-text>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { BarChart } from 'vue-chart-3';
import { Chart, registerables } from 'chart.js';
import { MetricasService } from '@/services/MetricasService';
import { ref, computed, onMounted } from 'vue';
import { watch } from 'vue';
Chart.register(...registerables);

const metricaSeleccionada = ref('plataRecaudada');

const empty = { labels: [], datasets: [] };
const plataRecaudada       = ref({ ...empty });
const clasesCanceladas     = ref({ ...empty });
const clasesConMensualidad = ref({ ...empty });
const fechaInicio = ref('');
const fechaFin = ref('');

// Mostrar el filtro solo en métricas que lo soporten
const mostrarFiltroFecha = computed(() =>
  ['clasesCanceladas', 'plataRecaudada', 'clasesConMensualidad'].includes(metricaSeleccionada.value)
);

const cargarConFiltro = async () => {
  if (metricaSeleccionada.value === 'clasesCanceladas') {
    await clasesMasCanceladasPorFecha(fechaInicio.value, fechaFin.value);
  } else if (metricaSeleccionada.value === 'plataRecaudada') {
    await plataRecaudadaPorFecha(fechaInicio.value, fechaFin.value);
  } else if (metricaSeleccionada.value === 'clasesConMensualidad') {
    await clasesConMensualidadPorFecha(fechaInicio.value, fechaFin.value);
  }
};

const limpiarFiltro = () => {
  fechaInicio.value = '';
  fechaFin.value = '';
  // Recarga sin filtro
  if (metricaSeleccionada.value === 'clasesCanceladas') cargarMetricasClases();
  else if (metricaSeleccionada.value === 'plataRecaudada') cargarMetricaPlataRecaudada();
  else if (metricaSeleccionada.value === 'clasesConMensualidad') cargarMetricasClasesConMensualidad();
};
watch(metricaSeleccionada, () => {
  fechaInicio.value = '';
  fechaFin.value = '';
});
// Computed que expone titulo, subtitulo y datos según la selección
const metricaActual = computed(() => ({
  plataRecaudada: {
    titulo: 'Métricas de ventas',
    subtitulo: 'Total recaudado por actividad',
    datos: plataRecaudada.value,
  },
  clasesCanceladas: {
    titulo: 'Métricas de clases',
    subtitulo: 'Clases canceladas por tipo',
    datos: clasesCanceladas.value,
  },
  clasesConMensualidad: {
    titulo: 'Clases con mensualidad',
    subtitulo: 'Clases con más mensualidades registradas',
    datos: clasesConMensualidad.value,
  },
})[metricaSeleccionada.value]);

onMounted(() => {
  cargarMetricasClases();
  cargarMetricaPlataRecaudada();
  cargarMetricasClasesConMensualidad();
});

const cargarMetricasClases = async () => {
  try {
    const { data } = await MetricasService.clasesMasCanceladas();
    clasesCanceladas.value = {
      labels: data.map(i => `${i.actividad} (${i.dia} ${i.hora})`),
      datasets: [{ label: 'Clases canceladas', data: data.map(i => i.cancelaciones), backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};

const cargarMetricaPlataRecaudada = async () => {
  try {
    const { data } = await MetricasService.plataRecaudada();
    const por = data.reduce((acc, i) => { acc[i.actividad_nombre] = (acc[i.actividad_nombre] || 0) + i.monto; return acc; }, {});
    plataRecaudada.value = {
      labels: Object.keys(por),
      datasets: [{ label: 'Plata recaudada', data: Object.values(por), backgroundColor: 'rgba(54, 162, 235, 0.2)', borderColor: 'rgba(54, 162, 235, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};

const cargarMetricasClasesConMensualidad = async () => {
  try {
    const clasesID = { 1: 'Yoga', 2: 'Funcional', 3: 'Pilates' };
    const { data } = await MetricasService.clasesConMensualidad();
    const por = data.reduce((acc, i) => { acc[i.clase_id] = (acc[i.clase_id] || 0) + i.cantidad_asistencias; return acc; }, {});
    clasesConMensualidad.value = {
      labels: Object.keys(por).map(id => clasesID[id]),
      datasets: [{ label: 'Clases con mensualidad', data: Object.values(por), backgroundColor: 'rgba(75, 192, 192, 0.2)', borderColor: 'rgba(75, 192, 192, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};

const cargarMetricasClasesFecha = async (fecha_inicio, fecha_fin) => {
  try {
    const { data } = await MetricasService.clasesMasCanceladas(fecha_inicio, fecha_fin);
    clasesCanceladas.value = {
      labels: data.map(i => `${i.actividad} (${i.dia} ${i.hora})`),
      datasets: [{ label: 'Clases canceladas', data: data.map(i => i.cancelaciones), backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};

const clasesMasCanceladasPorFecha = async (fecha_inicio, fecha_fin) => {
  try {
    const { data } = await MetricasService.clasesMasCanceladasPorFecha(fecha_inicio, fecha_fin);
    clasesCanceladas.value = {
      labels: data.map(i => `${i.actividad} (${i.dia} ${i.hora})`),
      datasets: [{ label: 'Clases canceladas', data: data.map(i => i.cancelaciones), backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};

const plataRecaudadaPorFecha = async (fecha_inicio, fecha_fin) => {
  try {
    const { data } = await MetricasService.plataRecaudadaPorFecha(fecha_inicio, fecha_fin);
    const por = data.reduce((acc, i) => { acc[i.actividad_nombre] = (acc[i.actividad_nombre] || 0) + i.monto; return acc; }, {});
    plataRecaudada.value = {
      labels: Object.keys(por),
      datasets: [{ label: 'Plata recaudada', data: Object.values(por), backgroundColor: 'rgba(54, 162, 235, 0.2)', borderColor: 'rgba(54, 162, 235, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};

const clasesConMensualidadPorFecha = async (fecha_inicio, fecha_fin) => {
  try {
    const clasesID = { 1: 'Yoga', 2: 'Funcional', 3: 'Pilates' };
    const { data } = await MetricasService.clasesConMensualidadPorFecha(fecha_inicio, fecha_fin);
    const por = data.reduce((acc, i) => { acc[i.clase_id] = (acc[i.clase_id] || 0) + i.cantidad_asistencias; return acc; }, {});
    clasesConMensualidad.value = {
      labels: Object.keys(por).map(id => clasesID[id]),
      datasets: [{ label: 'Clases con mensualidad', data: Object.values(por), backgroundColor: 'rgba(75, 192, 192, 0.2)', borderColor: 'rgba(75, 192, 192, 1)', borderWidth: 1 }],
    };
  } catch (e) { console.error(e); }
};
</script>