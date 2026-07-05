import os
from pathlib import Path

def copiar_texto_de_carpeta(ruta_carpeta, archivo_salida):
    carpeta = Path(ruta_carpeta)
    
    if not carpeta.exists() or not carpeta.is_dir():
        print(f"Error: La carpeta '{ruta_carpeta}' no existe.")
        return

    # Convertimos el nombre de salida a minúsculas para comparar con seguridad
    nombre_archivo_excluido = Path(archivo_salida).name.lower()
    
    # También obtenemos el nombre de este script de Python por si acaso
    nombre_script_actual = Path(__file__).name.lower()

    with open(archivo_salida, 'w', encoding='utf-8') as destino:
        archivos_encontrados = 0
        
        for archivo in carpeta.rglob('*.py'):
            if not archivo.is_file():
                continue

            es_archivo_salida = archivo.name.lower() == nombre_archivo_excluido
            es_propio_script = archivo.name.lower() == nombre_script_actual

            if es_archivo_salida or es_propio_script:
                continue

            archivos_encontrados += 1
            destino.write(f"=== CONTENIDO DE: {archivo.relative_to(carpeta)} ===\n\n")

            try:
                with open(archivo, 'r', encoding='utf-8') as origen:
                    destino.write(origen.read())
            except Exception as e:
                destino.write(f"[Error leyendo este archivo: {e}]")

            destino.write("\n\n" + "="*40 + "\n\n")

        print(f"Proceso terminado. Se copiaron {archivos_encontrados} archivos en '{archivo_salida}'.")

# --- CONFIGURACIÓN ---
ruta_de_tu_carpeta = "."  # El punto indica que busque en la misma carpeta donde está el script
archivo_resultado = "todo_el_texto_unido.txt"

# Ejecutar la función
copiar_texto_de_carpeta(ruta_de_tu_carpeta, archivo_resultado)
