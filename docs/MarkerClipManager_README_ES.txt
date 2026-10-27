MarkerClipManager — Administrador de Marcadores de Línea de Tiempo y Clips para DaVinci Resolve
===============================================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.7
MIT License — see the script header

QUÉ HACE
--------
Una sola ventana para ver y administrar todos los marcadores en una línea de tiempo de Resolve:
marcadores de regla (nivel de línea de tiempo) y marcadores colocados en clips individuales,
en todas las pistas de video y audio.

Para cada marcador muestra: gráfico de marcador (misma forma nativa que Resolve),
pista, TC entrada, TC salida, duración, color, nombre, palabra clave, nota.

CARACTERÍSTICAS
---------------
- Selecciona uno o varios marcadores y cambia el color, cambia la pista
  (incluido hacia/desde la regla "TIMELINE"), elimínalos
- Edita Nombre, Palabra clave y Nota directamente en la tabla (doble clic),
  incluso en varios marcadores seleccionados a la vez
- La tecla Supr hace lo mismo que el botón Eliminar, con una confirmación que
  puedes desactivar
- Deshacer y rehacer con Cmd+Z / Ctrl+Z, más un panel History: haz doble clic
  en un paso anterior para volver directamente allí. Solo cubre la sesión
  actual y se borra al cerrar el script
- Filtra por color, pista, autor/nombre o palabra clave
- Exporta e importa marcadores en CSV
- Haz clic en una fila: el cabezal de reproducción salta a ese marcador
- Interfaz disponible en 12 idiomas: arranca en el idioma de tu sistema si hay
  coincidencia, si no en inglés, y puedes cambiarlo desde el menú de la parte
  superior de la ventana (tiene efecto al reiniciar el script)

REQUISITOS
----------
- DaVinci Resolve 19/20 (macOS)
- Python 3 instalado en el sistema
- PySide6 (instalado automáticamente por el script de configuración a continuación — no se necesitan
  pasos manuales)

INSTALACIÓN (una sola vez)
--------------------------
1. Descarga el instalador para tu sistema
2. macOS: CLIC DERECHO en el archivo .command y elige "Abrir" — no doble clic,
   que macOS bloquea porque el archivo no está firmado con un certificado de
   desarrollador de Apple
   Windows: doble clic en el archivo .cmd; si SmartScreen avisa, elige "Más
   información" y luego "Ejecutar de todas formas"
3. El instalador copia los archivos y después prepara el entorno de Python que
   necesita el script (esta parte requiere conexión a internet y tarda alrededor
   de un minuto)
4. Si esa segunda parte falla — sin conexión, o sin Python — los archivos
   quedan instalados correctamente igualmente: abre la carpeta instalada y
   ejecuta "MarkerClipManager_Setup.command" (macOS) o
   "MarkerClipManager_Setup_Windows.cmd" (Windows) cuando puedas
5. Listo. Las actualizaciones se instalan del mismo modo, sobre la versión
   anterior, y tus ajustes quedan intactos

USO
---
En DaVinci Resolve: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(el script se encuentra en la subcarpeta "MarkerClipManager" dentro de Comp, por lo que aparece
en el menú como un submenú con el mismo nombre)

LIMITACIONES CONOCIDAS
----------------------
- El marcador en la tabla es un icono recreado dibujado por el script, no
  el icono oficial de Resolve (no expuesto por la API). Los colores son los
  valores hexadecimales exactos proporcionados por el usuario — solo la forma
  del icono sigue siendo una aproximación
- "Palabra clave" no es un campo de marcador nativo de Resolve: se almacena
  en un campo de marcador interno (customData), invisible al panel Marcador
  nativo de Resolve — legible/escribible solo por este script
- Timecode lee fps y modo Drop Frame/Non-Drop Frame directamente desde la
  línea de tiempo activa del proyecto (29.97 y 59.94 DF manejados correctamente
  con el algoritmo SMPTE estándar); en fps no estándar las matemáticas siguen siendo aproximadas
- La importación/exportación de EDL no se maneja con este script: use la
  función nativa de Resolve (Timeline > Markers > Export/Import)
- Mover un marcador a una pista de video/audio requiere que ya exista un clip
  en esa posición

SOPORTE
-------
Informes de errores: use el botón 🐛 en la aplicación (abre un email precargado para
tomfilmeditor.tools@gmail.com)
Si desea apoyar el desarrollo: botón ☕ en la aplicación, o
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
