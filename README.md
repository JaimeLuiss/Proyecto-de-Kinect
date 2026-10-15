# Piano Virtual con Hand Tracking

Proyecto en Python que convierte la cámara web en un piano virtual interactivo usando detección de manos con MediaPipe y OpenCV. El sistema detecta la punta del dedo índice y permite tocar notas musicales al posicionarlo sobre un teclado virtual.

## Descripción

Esta aplicación crea una experiencia de piano con interacción por gestos. En lugar de usar un teclado físico, el usuario mueve la mano frente a la webcam y toca las notas al colocar el dedo índice sobre cada tecla del piano. Cada nota se reproduce con audio en tiempo real y se incluye una melodía de demostración.

## Funcionalidades

- Detección de manos con MediaPipe Hand Landmarker.
- Teclado virtual grande con cinco notas: Do, Re, Mi, Fa y Sol.
- Reproducción de audio con el sistema Windows usando winsound.
- Debounce para evitar sonidos repetidos al mantener una nota tocada.
- Soporte para dos manos simultáneas.
- Interfaz visual con fondo oscuro, encabezado y piano en pantalla.
- Tecla rápida para reproducir la melodía de ejemplo "Jingle Bells".
- Detección automática de cámaras disponibles en el sistema.

## Tecnologías

- Python 3.9+
- OpenCV
- MediaPipe
- NumPy
- Windows API: winsound

## Requisitos previos

- Python 3.9 o superior
- Cámara web funcional
- Sistema operativo Windows (por el uso de winsound)
- Conexión a internet para descargar el modelo de MediaPipe al ejecutar el programa por primera vez

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/piano_virtual_hand_tracking.git
cd piano_virtual_hand_tracking
```

2. Crea un entorno virtual (opcional, pero recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

Al iniciar, la aplicación descargará el modelo de MediaPipe si aún no existe y abrirá la cámara.

## Controles

- M: reproduce la melodía de demostración.
- Q: cierra la aplicación.

## Notas por defecto

La aplicación usa las siguientes frecuencias:

- Do = 261.63 Hz
- Re = 293.66 Hz
- Mi = 329.63 Hz
- Fa = 349.23 Hz
- Sol = 392.00 Hz

## Cómo usarlo

1. Ejecuta la aplicación.
2. Coloca tu mano frente a la cámara.
3. Extiende el dedo índice y mueve la punta sobre las teclas del piano.
4. Cuando el dedo esté sobre una nota, la tecla se resalta y suena la nota.
5. Presiona M para escuchar la melodía automática.

## Estructura del proyecto

```text
piano_virtual_hand_tracking/
├── main.py
├── hand_landmarker.task
├── README.md
├── requirements.txt
└── .venv/   (opcional)
```

## Flujo principal del programa

- Se inicializa la cámara y se abre la captura de video.
- Se carga el modelo de Hand Landmarker de MediaPipe.
- En cada frame, se detectan manos y puntos clave.
- Se obtiene la posición del dedo índice.
- Se compara la coordenada con los rectángulos de cada tecla.
- Si el dedo entra en una nota, se activa la reproducción del sonido y se evita el rebote con un debounce.
- La interfaz dibuja el teclado y la mano detectada en la pantalla.

## Solución de problemas

### La cámara no se abre
- Prueba otros índices de cámara: 0, 1, 2 o 3.
- Verifica que la cámara no esté siendo usada por otra aplicación.
- Revisa permisos de cámara en el sistema.

### La mano no se detecta bien
- Mejora la iluminación del lugar.
- Usa un fondo claro y uniforme.
- Mantén la mano en el rango de la cámara y en una posición visible.

### Error al instalar dependencias
- Verifica que Python esté instalado correctamente.
- Actualiza pip:

```bash
python -m pip install --upgrade pip
```

### El audio no funciona
- Este proyecto usa winsound, por lo que está pensado para Windows.
- Si usas otro sistema operativo, deberás reemplazar winsound por una librería compatible como pygame o sounddevice.

## Mejoras futuras

- Añadir más octavas y notas musicales.
- Mejorar la detección con seguimiento más estable de la mano.
- Añadir animaciones visuales al tocar cada tecla.
- Soportar reconocimiento de varios dedos o gestos.
- Integrar sonidos más ricos mediante sintetizadores o archivos WAV.
- Agregar modo de práctica para seguir melodías o acordes.

## Licencia

Este proyecto se entrega con fines educativos y de demostración. Puedes adaptarlo y ampliarlo según tus necesidades.

## Repositorio

Puedes clonar o explorar el proyecto desde tu entorno local.
