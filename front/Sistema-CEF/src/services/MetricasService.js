import apiClient from './api.js'

export const MetricasService = {
  clasesMasCanceladas: async () => 
    apiClient.get('/metricas/clases_mas_canceladas'),
    
  clasesMasCanceladasPorFecha: async (fechaInicio, fechaFin) => 
    apiClient.get('/metricas/clases_mas_canceladas', { 
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin } 
    }),

  clasesConMensualidad: async () => 
    apiClient.get('/metricas/clases_con_mensualidad'),
    
  clasesConMensualidadPorFecha: async (fechaInicio, fechaFin) => 
    apiClient.get('/metricas/clases_con_mensualidad', { 
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin } 
    }),

  plataRecaudada: async () => 
    apiClient.get('/metricas/plata_recaudada'),
    
  plataRecaudadaPorFecha: async (fechaInicio, fechaFin) => 
    apiClient.get('/metricas/plata_recaudada', { 
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin } 
    }),
}
