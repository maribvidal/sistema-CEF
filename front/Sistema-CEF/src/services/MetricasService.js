import apiClient from './api.js'

export const MetricasService = {
  clasesMasCanceladas: async () => 
    apiClient.get('/metricas/clases_mas_canceladas'),
    
  clasesMasCanceladasPorFecha: async (fecha_inicio, fecha_fin) => 
    apiClient.get('/metricas/clases_mas_canceladas/con_fechas', { 
    params: { fecha_inicio: fecha_inicio, fecha_fin: fecha_fin } 
    }),

  clasesConMensualidad: async () => 
    apiClient.get('/metricas/clases_con_mensualidad'),
    
  clasesConMensualidadPorFecha: async (fecha_inicio, fecha_fin) => 
    apiClient.get('/metricas/clases_con_mensualidad/con_fechas', { 
      params: { fecha_inicio: fecha_inicio, fecha_fin: fecha_fin } 
    }),

  plataRecaudada: async () => 
    apiClient.get('/metricas/plata_recaudada'),
    
  plataRecaudadaPorFecha: async (fecha_inicio, fecha_fin) => 
    apiClient.get('/metricas/plata_recaudada/con_fechas', { 
      params: { fecha_inicio: fecha_inicio, fecha_fin: fecha_fin } 
    }),
}
