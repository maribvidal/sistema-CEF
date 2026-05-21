/**
 * Convierte una fecha en formato "mm/dd/yyyy" o "dd/mm/yyyy" a "dd-mm-yyyy".
 * Regla para entradas ambiguas (ej. 05/06/2026): se interpreta como dd/mm/yyyy.
 * @param {string} dateString - La fecha de entrada.
 * @returns {string} Fecha en formato "dd-mm-yyyy" o el string original si es inválido.
 */
export function formatDisplayDate(dateString) {
  if (!dateString || typeof dateString !== 'string') {
    return ''
  }

  const parsedDate = parseFlexibleDate(dateString)
  if (!parsedDate) {
    return dateString
  }

  const day = String(parsedDate.getDate()).padStart(2, '0')
  const month = String(parsedDate.getMonth() + 1).padStart(2, '0')
  const year = parsedDate.getFullYear()

  return `${day}-${month}-${year}`
}

/**
 * Devuelve la fecha actual en formato "dd-mm-yyyy".
 * @returns {string} La fecha formateada.
 */
export function getCurrentDateFormatted() {
  const hoy = new Date()
  const dia = String(hoy.getDate()).padStart(2, '0')
  const mes = String(hoy.getMonth() + 1).padStart(2, '0')
  const anio = hoy.getFullYear()
  return `${dia}-${mes}-${anio}`
}

/**
 * Parsea un string de fecha en formato "dd/mm/yyyy" o "mm/dd/yyyy".
 * Regla para entradas ambiguas (ej. 05/06/2026): se interpreta como dd/mm/yyyy.
 * @param {string} dateString - La fecha de entrada.
 * @returns {Date|null} Un objeto Date válido o null si el formato es incorrecto.
 */
export function parseDMYDate(dateString) {
  return parseFlexibleDate(dateString)
}

function parseFlexibleDate(dateString) {
  if (!dateString || typeof dateString !== 'string') return null

  const match = dateString.trim().match(/^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$/)
  if (!match) return null

  const first = parseInt(match[1], 10)
  const second = parseInt(match[2], 10)
  const year = parseInt(match[3], 10)

  let day
  let month

  // Si el primer valor no puede ser mes, asumimos dd/mm.
  if (first > 12 && second <= 12) {
    day = first
    month = second
  } else if (second > 12 && first <= 12) {
    // Si el segundo valor no puede ser mes, asumimos mm/dd.
    month = first
    day = second
  } else {
    // Caso ambiguo (ambos <= 12): por defecto interpretamos dd/mm.
    day = first
    month = second
  }

  if (month < 1 || month > 12 || day < 1 || day > 31) {
    return null
  }

  const parsed = new Date(year, month - 1, day)
  if (
    Number.isNaN(parsed.getTime()) ||
    parsed.getFullYear() !== year ||
    parsed.getMonth() !== month - 1 ||
    parsed.getDate() !== day
  ) {
    return null
  }

  return parsed
}

/**
 * Formatea una fecha para mostrarla como "16 de Junio de 1997".
 * @param {string} dateString - La fecha de entrada.
 * @returns {string} Fecha en formato texto español.
 */
export function formatSpanishDate(dateString) {
  if (!dateString) return ''

  let dateObj
  // Si ya es un formato YYYY-MM-DD
  if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
    const [year, month, day] = dateString.split('-')
    dateObj = new Date(year, month - 1, day)
  } else {
    dateObj = parseFlexibleDate(dateString)
  }

  if (!dateObj) return dateString

  const meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ]

  const day = dateObj.getDate()
  const month = meses[dateObj.getMonth()]
  const year = dateObj.getFullYear()

  return `${day} de ${month} de ${year}`
}

/**
 * Convierte una fecha a formato YYYY-MM-DD apto para SQLite / Backend.
 * @param {string} dateString - La fecha de entrada.
 * @returns {string} Fecha en formato "YYYY-MM-DD"
 */
export function formatDateForBackend(dateString) {
  if (!dateString) return ''
  
  // Si la fecha ya viene del input type="date", ya es "YYYY-MM-DD"
  if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
    return dateString
  }

  const dateObj = parseFlexibleDate(dateString)
  if (!dateObj) return dateString // falla graciosa devolviendo el original

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