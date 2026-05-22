/**
 * Constante que contiene los nombres de los meses en español.
 */
const MESES_ESPANOL = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

/**
 * Verifica si un objeto Date fue creado con valores válidos y no sufrió desbordamientos nativos
 * (por ejemplo: intentar crear 31 de Febrero y que JavaScript lo convierta en 3 de Marzo).
 * 
 * @param {Date} dateObj - El objeto fecha a evaluar.
 * @param {number} year - Año esperado.
 * @param {number} monthIndex - Índice del mes esperado (0-11).
 * @param {number} day - Día esperado.
 * @returns {boolean} Retorna verdadero si es exactamente la fecha deseada.
 */
function isValidDate(dateObj, year, monthIndex, day) {
  return (
    !Number.isNaN(dateObj.getTime()) &&
    dateObj.getFullYear() === year &&
    dateObj.getMonth() === monthIndex &&
    dateObj.getDate() === day
  )
}

/**
 * Parsea una fecha suministrada de diferentes formas:
 * - Objeto `Date` de JavaScript.
 * - String en formato estándar backend (ISO corto): "YYYY-MM-DD".
 * - String en formato "dd/mm/yyyy" o "mm/dd/yyyy" (con '/' ó '-').
 * 
 * Regla para entradas ambiguas (ej. "05/06/2026"): se interpreta como dd/mm/yyyy.
 * 
 * @param {string|Date} dateInput - La fecha de entrada a parsear.
 * @returns {Date|null} Un objeto Date válido o null si su formato es irreconocible o incorrecto.
 */
function parseFlexibleDate(dateInput) {
  if (!dateInput) return null

  // Si ya es un objeto Date
  if (dateInput instanceof Date) {
    return Number.isNaN(dateInput.getTime()) ? null : dateInput
  }

  if (typeof dateInput !== 'string') return null

  // Si está en formato tipo base de datos/input date nativo "YYYY-MM-DD"
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateInput)) {
    const [year, month, day] = dateInput.split('-').map(Number)
    const parsed = new Date(year, month - 1, day)
    return isValidDate(parsed, year, month - 1, day) ? parsed : null
  }

  // Soporte para "dd/mm/yyyy", "mm/dd/yyyy" usando guiones o barras
  const match = dateInput.trim().match(/^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$/)
  if (!match) return null

  const first = parseInt(match[1], 10)
  const second = parseInt(match[2], 10)
  const year = parseInt(match[3], 10)

  let day, month

  // Lógica para descubrir cuál es el día y cuál el mes garantizando coherencia
  if (first > 12 && second <= 12) {
    day = first
    month = second
  } else if (second > 12 && first <= 12) {
    month = first
    day = second
  } else {
    // Caso ambiguo (ambos <= 12): por defecto interpretamos dd/mm
    day = first
    month = second
  }

  // Validar límites básicos obvios antes de delegar en el objeto Date
  if (month < 1 || month > 12 || day < 1 || day > 31) {
    return null
  }

  const parsed = new Date(year, month - 1, day)
  return isValidDate(parsed, year, month - 1, day) ? parsed : null
}

/**
 * Convierte una fecha a la visualización estándar del frontend: "dd-mm-yyyy".
 * Si la fecha original no es válida, la devuelve como está (útil para fallar de forma amable).
 * 
 * @param {string|Date} dateInput - La fecha de entrada.
 * @returns {string} Fecha en formato "dd-mm-yyyy" o el valor original si erró.
 */
export function formatDisplayDate(dateInput) {
  const parsedDate = parseFlexibleDate(dateInput)
  if (!parsedDate) return typeof dateInput === 'string' ? dateInput : ''

  const day = String(parsedDate.getDate()).padStart(2, '0')
  const month = String(parsedDate.getMonth() + 1).padStart(2, '0')
  const year = parsedDate.getFullYear()

  return `${day}-${month}-${year}`
}

/**
 * Devuelve la fecha actual con el formato estándar de visualización "dd-mm-yyyy".
 * 
 * @returns {string} La fecha actual formateada.
 */
export function getCurrentDateFormatted() {
  return formatDisplayDate(new Date())
}

/**
 * Expone la validación y el parseo de fechas al exterior.
 * 
 * @param {string|Date} dateString - La fecha de entrada.
 * @returns {Date|null} Un objeto Date válido o null si el formato es incorrecto.
 */
export function parseDMYDate(dateString) {
  return parseFlexibleDate(dateString)
}

/**
 * Formatea una fecha obteniéndola en un texto legible de formato largo, 
 * por ejemplo: "16 de Junio de 1997".
 * 
 * @param {string|Date} dateInput - La fecha a formatear.
 * @returns {string} La fecha en formato texto español amigable, o el string original.
 */
export function formatSpanishDate(dateInput) {
  const dateObj = parseFlexibleDate(dateInput)
  if (!dateObj) return typeof dateInput === 'string' ? dateInput : ''

  const day = dateObj.getDate()
  const month = MESES_ESPANOL[dateObj.getMonth()]
  const year = dateObj.getFullYear()

  return `${day} de ${month} de ${year}`
}

/**
 * Prepara una fecha ingresada para ser enviada y guardada en el backend 
 * convirtiéndola a la norma ISO corta ("YYYY-MM-DD").
 * 
 * @param {string|Date} dateInput - La fecha a convertir.
 * @returns {string} Fecha en formato "YYYY-MM-DD" para ser almacenada correctamente.
 */
export function formatDateForBackend(dateInput) {
  const dateObj = parseFlexibleDate(dateInput)
  if (!dateObj) return typeof dateInput === 'string' ? dateInput : ''

  const year = dateObj.getFullYear()
  const month = String(dateObj.getMonth() + 1).padStart(2, '0')
  const day = String(dateObj.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const DateFormatterService = {
  formatDisplayDate,
  getCurrentDateFormatted,
  parseDMYDate,
  formatSpanishDate,
  formatDateForBackend,
}

export default DateFormatterService