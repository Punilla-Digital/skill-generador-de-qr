# Generador de QR

Generación real y verificación de QR con Python: con logo, sin logo o ambas versiones, colores personalizados, PNG, SVG, vista previa, informe de validación y ZIP.

- Instrucciones: [SKILL.md](SKILL.md).
- Recursos e iconos: incluidos en `assets/` y `agents/`.
- Referencias: `references/`.

## Requisitos

Python y dependencias de scripts/requirements.txt: qrcode, Pillow, CairoSVG y zxing-cpp. CairoSVG puede requerir Cairo instalado en el sistema. No dibuja QR con generación de imágenes.

## Uso e instalación

1. Descargar el repositorio.
2. Usar la carpeta del repositorio como carpeta de la skill.
3. En un agente compatible, copiar la carpeta completa con el nombre `generar-qr` a su directorio de skills. Conservar scripts, referencias y recursos junto al SKILL.md. Si el entorno ofrece importación, seguir su procedimiento; publicar en GitHub no instala automáticamente la skill en ChatGPT.
4. Resolver las rutas de recursos desde la carpeta de la skill. En otros asistentes, adjuntar solo SKILL.md no carga automáticamente scripts ni imágenes.

Las menciones a habilidades de PDF o generación de imágenes requieren herramientas equivalentes en el entorno; no se incluyen habilidades de terceros. Los iconos de agents/openai.yaml dependen del soporte del agente.

## Ejemplo

> Generá QR de https://punilladigital.com.ar/ con y sin logo, en negro y naranja.

## Identidad y recursos

Conservar los logos y las reglas incluidas. Aplicar los cambios de marca, colores o formato que admita la habilidad y solicite el usuario. No inventar un logo ni presentar archivos como generados antes de crearlos y verificarlos.

El logo predeterminado del generador es un monograma QR, no el logo comercial de Punilla Digital. Se puede adjuntar un logo propio. Mostrar siempre la URL exacta codificada al entregar los QR.

## Origen y alcance

Copia de la habilidad personal de Punilla Digital aprobada para este repositorio el 15/10/2026. Se preservan sus instrucciones y recursos funcionales; esta publicación no modifica la habilidad instalada en Complementos.

[Punilla Digital](https://punilladigital.com.ar/) · Consultar [LICENSE](LICENSE).
