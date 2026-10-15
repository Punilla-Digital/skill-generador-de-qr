---
name: generar-qr
description: Generar códigos QR reales desde enlaces, WhatsApp u otros contenidos con Python, con y sin logo central, colores y versiones PNG y SVG verificadas. Usar al pedir QR para flyers, tarjetas, carteles o catálogos; entregar archivos individuales, vista previa y ZIP.
---
# Generador de QR

Mostrar siempre las opciones disponibles: contenido/enlace; logo propio a color o monograma QR negro incluido; modo con logo, sin logo o ambas versiones; negro sobre blanco y blanco sobre negro (ambos por defecto); colores adicionales como verde WhatsApp o HEX de marca; tamaño (módulos de 24 píxeles por defecto); PNG y SVG. Si ya hay enlace, proceder con los valores predeterminados sin exigir una respuesta. Si falta contenido, pedirlo. No cambiar, acortar ni visitar el enlace; codificarlo literalmente. Confirmar solo ambigüedades que cambien su destino.

Ejecutar código real, nunca dibujar QR con generación de imágenes. Requerir ejecución de Python y dependencias de scripts/requirements.txt; instalarlas si faltan y el entorno lo permite. Si no hay ejecución disponible, explicar la limitación sin afirmar que se generaron archivos.

Ejecutar desde cualquier carpeta:
```bash
python /ruta/generar-qr/scripts/generate.py --url 'https://ejemplo.com/' --out /ruta/salida
```
Usar una carpeta de salida nueva o vacía; mantener el logo fuente fuera de ella. Elegir `--logo-mode with`, `--logo-mode without` o `--logo-mode both`. Por defecto usar `with` para conservar el comportamiento existente. Si se piden con y sin logo, usar `both` en una sola ejecución, con vista previa e informe y ZIP comunes. En modo sin logo no cargar ningún logo, no colocar placa central ni borrar módulos; conservar el QR completo. Identificar archivos con los sufijos `-con-logo` y `-sin-logo`.

Opciones adicionales: `--logo /ruta/logo.png` (PNG, JPEG o WebP; conservar sus colores), `--color '#128C4A'` (repetible), `--scale 24`. Para SVG de logo, rasterizar primero con CairoSVG. No descargar logos sin autorización; usar el adjunto. No modificar colores de marca automáticamente.

El script usa corrección H, margen de cuatro módulos y logo pequeño con placa blanca. Valida el PNG final y una rasterización independiente de cada SVG con ZXing, comparando el contenido exacto. Para la versión invertida intenta también la inversión de luminancia. Reducir el logo si falla; si persiste, detener y ofrecer cambiar color, tamaño o quitar logo. Nunca entregar un archivo fallido como verificado. Los QR blancos tienen compatibilidad variable entre lectores: informar brevemente y recomendar el negro para máxima compatibilidad. No prometer lectura universal ni garantías de impresión.

Comprobar visualmente preview.png. Mantener toda la zona de silencio al colocar el QR. No recortar ni deformar. Para impresión o usos críticos sugerir prueba con teléfonos reales al tamaño final.

Entregar enlaces descargables separados a TODOS los PNG y SVG, mostrar preview.png y enlazar qr-completo.zip. Guardar entregables con el mecanismo persistente del entorno. Mostrar siempre en la respuesta final la URL exacta codificada en los QR, como enlace clicable, con la etiqueta «URL de los QR». No sustituirla por un título ni por el destino supuesto de una redirección. Si el contenido no es una URL, mostrar el contenido exacto con la etiqueta «Contenido de los QR». Si se generan QR con distintos destinos, identificar qué URL o contenido corresponde a cada grupo de archivos. Incluir resultado real de validación; no exponer detalles internos innecesarios. El ZIP contiene QR, vista previa e informe de validación. No incluir el enlace del QR en servicios externos de generación.
