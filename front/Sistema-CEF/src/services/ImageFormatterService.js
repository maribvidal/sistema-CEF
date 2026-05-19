/**
 * Detecta el tipo de imagen a partir de una cadena Base64 y devuelve una URL de datos completa.
 * Esta función es genérica y puede usarse para avatares, portadas de artículos, etc.
 * @param {string} base64String La cadena Base64 de la imagen, sin el prefijo "data:image...".
 * @returns {string|null} La URL de datos completa (ej. "data:image/jpeg;base64,...") o null si la entrada es inválida.
 */
export function createImageSrcFromBase64(base64String) {
  if (!base64String || typeof base64String !== 'string') {
    return null
  }

  // Los "números mágicos" al inicio de la cadena Base64 identifican el tipo de archivo.
  if (base64String.startsWith('/9j/')) return `data:image/jpeg;base64,${base64String}`
  if (base64String.startsWith('iVBORw0KGgo=')) return `data:image/png;base64,${base64String}`
  if (base64String.startsWith('R0lGODlh')) return `data:image/gif;base64,${base64String}`
  if (base64String.startsWith('UklGR')) return `data:image/webp;base64,${base64String}`
  if (base64String.startsWith('PD94bWwgdmVyc2lvbj0iMS4wI'))
    return `data:image/svg+xml;base64,${base64String}`

  // Si no se reconoce, se asume JPEG como último recurso o se devuelve null si se prefiere ser estricto.
  console.warn('Tipo de imagen Base64 no reconocido, se asume JPEG.')
  return `data:image/jpeg;base64,${base64String}`
}