/**
 * Parsea un string de fecha en formato "dd/MM/yyyy" y lo formatea a un formato legible.
 * @param {string} dateString - La fecha en formato "dd/MM/yyyy".
 * @returns {string} La fecha formateada (ej: "16 de agosto de 2025") o el string original si el formato es inválido.
 */
export function formatDisplayDate(dateString) {
  // Si no hay fecha o no es un string, devolvemos un string vacío.
  if (!dateString || typeof dateString !== 'string') {
    return ''
  }

  // 1. Dividimos el string "dd/MM/yyyy" en sus partes.
  const parts = dateString.split('/')

  // 2. Verificamos que el formato sea correcto (3 partes).
  if (parts.length !== 3) {
    // Si no tiene el formato esperado, devolvemos el string original.
    return dateString
  }

  const day = parseInt(parts[0], 10)
  const month = parseInt(parts[1], 10)
  const year = parseInt(parts[2], 10)

  // 3. Creamos un objeto Date usando las partes.
  //    Formato: new Date(año, mes - 1, día)
  //    ¡Importante! El mes en el constructor de Date es 0-indexado.
  const date = new Date(year, month - 1, day)

  // 4. Verificamos si la fecha resultante es válida.
  if (isNaN(date.getTime()) || date.getDate() !== day) {
    // La fecha no es válida (ej. "32/13/2025"), devolvemos el string original.
    return dateString
  }

  // 5. Ahora sí, formateamos la fecha con el formato deseado.
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

/**
 * Devuelve la fecha actual en formato "dd/MM/yyyy".
 * @returns {string} La fecha formateada.
 */
export function getCurrentDateFormatted() {
  const hoy = new Date()
  const dia = String(hoy.getDate()).padStart(2, '0')
  const mes = String(hoy.getMonth() + 1).padStart(2, '0') // getMonth() es 0-11
  const anio = hoy.getFullYear()
  return `${dia}/${mes}/${anio}`
}

/**
 * Parsea un string de fecha en formato "dd/MM/yyyy" y devuelve un objeto Date.
 * @param {string} dateString - La fecha en formato "dd/MM/yyyy".
 * @returns {Date|null} Un objeto Date válido o null si el formato es incorrecto.
 */
export function parseDMYDate(dateString) {
  if (!dateString || typeof dateString !== 'string') return null

  const parts = dateString.split('/')
  if (parts.length !== 3) return null

  const day = parseInt(parts[0], 10)
  const month = parseInt(parts[1], 10)
  const year = parseInt(parts[2], 10)

  // El mes en el constructor de Date es 0-indexado (0=Enero).
  const date = new Date(year, month - 1, day)

  // Verificación para fechas inválidas como 32/13/2025
  if (isNaN(date.getTime()) || date.getDate() !== day) {
    return null
  }

  return date
}

// Exportamos un objeto para poder añadir más funciones en el futuro.
const DateFormatterService = {
  formatDisplayDate,
  getCurrentDateFormatted,
}

export default DateFormatterService