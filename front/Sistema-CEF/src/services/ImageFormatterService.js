/**
 * 1. Procesa un string Base64 "crudo" y le añade el prefijo correcto.
 * 
 * * @param {string} base64String La cadena Base64, sin el prefijo "data:image...".
 * @returns {string|null} La URL de datos completa o null si la entrada es inválida.
 */
export function createImageSrcFromBase64(base64String) {
  // 1. EL SALVAVIDAS: Si lo que llega es un objeto y tiene la propiedad 'contenido',
  // sacamos el texto y machacamos la variable para que deje de ser un objeto.
  if (typeof base64String === 'object' && base64String !== null && base64String.contenido) {
    base64String = base64String.contenido;
  }

  // Ahora sí, si imprimimos en consola, debería decir TIPO: string
  // console.log('🧐 DATOS YA FILTRADOS:', base64String.substring(0, 20) + '...', '| TIPO:', typeof base64String);

  // 2. Tu validación original (ahora la pasará sin problemas porque ya es un string)
  if (!base64String || typeof base64String !== 'string') {
    return null;
  }

  if (base64String.startsWith('data:image')) {
    return base64String;
  }

  if (base64String.startsWith('/9j/')) return `data:image/jpeg;base64,${base64String}`;
  if (base64String.startsWith('iVBORw0KGgo')) return `data:image/png;base64,${base64String}`;
  if (base64String.startsWith('R0lGODlh')) return `data:image/gif;base64,${base64String}`;
  if (base64String.startsWith('UklGR')) return `data:image/webp;base64,${base64String}`;
  if (base64String.startsWith('PD94bWwgdmVyc2lvbj0iMS4wI')) return `data:image/svg+xml;base64,${base64String}`;

  console.warn('Tipo de imagen Base64 no reconocido, se asume JPEG.');
  return `data:image/jpeg;base64,${base64String}`;
}

/**
 * 2. Convierte un objeto Blob o File a un Base64 válido (Data URL).
 * Se usa una Promesa porque la lectura de archivos en el navegador es asíncrona.
 * * @param {Blob|File} blob El archivo binario a convertir.
 * @returns {Promise<string>} Promesa que resuelve con el Base64 listo para usar.
 */
export function createBase64FromBlob(blob) {
  return new Promise((resolve, reject) => {
    if (!(blob instanceof Blob)) {
      reject(new Error('El parámetro no es un Blob o File válido.'));
      return;
    }

    const reader = new FileReader();
    
    // Cuando termina de leer, devuelve el resultado que ya incluye el prefijo "data:image..."
    reader.onloadend = () => resolve(reader.result);
    reader.onerror = () => reject(new Error('Error al leer el Blob.'));
    
    reader.readAsDataURL(blob);
  });
}

/**
 * 3. FUNCIÓN PRINCIPAL UNIFICADA (La que deberías llamar en tus componentes)
 * Detecta automáticamente si lo que le pasas es un Blob o un String y actúa en consecuencia.
 * * @param {string|Blob|File} imageInput La imagen recibida (puede ser string o blob)
 * @returns {Promise<string|null>} El "src" listo para poner en tu etiqueta <img>
 */
export async function getValidImageSrc(imageInput) {
  if (!imageInput) return null;

  // NUEVO: Si recibimos un objeto que tiene la propiedad 'contenido' (tu caso), 
  // extraemos el texto y sobrescribimos la variable.
  if (typeof imageInput === 'object' && imageInput !== null && imageInput.contenido) {
    imageInput = imageInput.contenido;
  }

  // Escenario A: Es un Blob o File
  if (imageInput instanceof Blob) {
    try {
      return await createBase64FromBlob(imageInput);
    } catch (error) {
      console.error('Error procesando el Blob de imagen:', error);
      return null;
    }
  }

  // Escenario B: Es una cadena de texto (¡Ahora sí pasará por aquí!)
  if (typeof imageInput === 'string') {
    return createImageSrcFromBase64(imageInput);
  }

  console.warn('Formato de entrada de imagen no soportado en getValidImageSrc');
  return null;
}