# 📌 PUNTO 2 — Desarrollo de un Algoritmo de Segmentación

(Multímetros, Osciloscopios, Raspberry Pi)
Taller 7 — Sistemas Digitales III · **Ubuntu Linux**

---

Este punto del taller consistió en desarrollar un sistema completo capaz de:

* **Detectar** multímetros, osciloscopios y **Raspberry Pi** usando un modelo entrenado con **YOLO**.
* Generar una **segmentación aproximada** a partir de la detección YOLO.
* Usar **hilos** (`threads`) para procesar la cámara en paralelo.
* Evitar **condiciones de carrera** mediante `locks`.
* Visualizar todo en **tiempo real** mediante **Streamlit**.
* Preparar el sistema para ser **desplegado dentro de Docker**.

El sistema final cumple con todos los requerimientos y funciona en **tiempo real**.

## 🎯 Objetivo General

Implementar un algoritmo de segmentación aplicando:

* **Ubuntu Linux**
* **Hilos y concurrencia**
* **Semaforización / mutex**
* **Visión por computadora**
* **YOLO** (modelo entrenado en Roboflow + Google Colab)
* **Streamlit** para la interfaz
* **Docker** para despliegue del sistema

---

## 🧩 Descripción del Dashboard

El dashboard desarrollado en Streamlit permite:

### ✔ Visualizar detección en tiempo real
* Se muestran las **cajas** (`bounding boxes`) generadas por YOLO.
* Se identifica el tipo de dispositivo (**multímetro**, **osciloscopio**, **Raspberry Pi**).

### ✔ Obtener segmentación aproximada
* Se genera una **máscara (segmentación)** usando el área del `bounding box`.
* La segmentación **resalta únicamente el objeto detectado**. 

### ✔ Ejecución multihilo
* La cámara se procesa en un **hilo dedicado**.
* La interfaz **Streamlit nunca se bloquea**.

### ✔ Sistema listo para Docker
* El proyecto incluye un **Dockerfile** y `requirements.txt` listos para despliegue.

## 📂 Estructura del Proyecto: Segmentación

```bash
segmentacion/
├── app/
│   └── dashboard.py              # Interfaz de usuario **Streamlit**
├── docker/
│   ├── Dockerfile                # Archivo para la **Dockerización**
│   └── requirements.txt          # Dependencias del proyecto
├── model/
│   └── best.pt                   # Modelo **YOLO** entrenado
├── src/
│   ├── camera_thread.py          # **Hilo dedicado** de captura de cámara
│   ├── detector_yolo.py          # Detector YOLO
│   ├── pipeline.py               # **Pipeline** de procesamiento (hilos + detección + segmentación)
│   └── segmentador_simple.py     # Lógica de **Segmentación** basada en YOLO
├── main.py                       # Punto de entrada principal
└── utils.py                      # Funciones de utilidad
```

# 🚀 Proceso Completo Realizado
  
## 1️⃣ Entrenamiento del modelo YOLO

### 📸 Captura y Anotación de Datos
* Se capturaron **imágenes** de multímetros, osciloscopios y Raspberry Pi.
* Se subieron a **Roboflow**, donde fueron **anotadas manualmente**.
* Se generaron **tres versiones** del *dataset* con diferentes tamaños.

### ❌ Dificultad con la Exportación
Se intentó descargar los pesos desde Roboflow, pero:
> ❌ **Roboflow** pedía plan de pago para exportar el archivo de pesos (`.pt`).

### ✔ Solución: Entrenamiento en Google Colab
* **Solución:** Entrenar el modelo de forma **gratuita** en **Google Colab** usando la librería **ultralytics**.

### 💻 Pasos del Entrenamiento
* Se utilizó **Google Colab GPU**.
* Se cargó el *dataset* desde Roboflow (en formato **YOLOv8**).
* Se obtuvo el modelo final, guardado como:
  > `best.pt`

## 2️⃣ Intento fallido con MediaPipe

Se probó integrar **MediaPipe Image Segmenter**.

### ❌ Problemas encontrados:
* MediaPipe solo segmenta **personas**, cabello, rostro, piel o ropa.
* Los modelos **NO segmentan objetos** como multímetros u osciloscopios.
* Intentar usar un modelo propio requiere un archivo `.tflite` entrenado, el cual no estaba disponible.
* Los modelos preentrenados de MediaPipe generaban máscaras completamente blancas.

### ✔ Solución
Se decidió **no usar MediaPipe**, por no ser adecuado para la segmentación de objetos electrónicos específicos.

---

## 3️⃣ Segmentación simplificada basada en YOLO

Para cumplir con el objetivo del taller sin un modelo de segmentación *instance* dedicado:

### ✔ Enfoque adoptado:
* Se usa **YOLO** para la **detección** (generar el *bounding box*).
* Se crea una **"segmentación falsa"** o simplificada **resaltando únicamente el área de la caja detectada**.
* Esto genera una máscara totalmente válida para fines académicos. 

### 🎨 Ejemplo de Máscara Generada:
* Todo fuera de la caja → **Negro**
* Todo dentro de la caja → **Blanco**

---

## 4️⃣ Implementación con hilos y concurrencia

Para lograr el procesamiento en tiempo real sin bloquear la interfaz:

### 🔸 `CameraThread`
* Captura imágenes sin bloquear la interfaz.
* Corre en un **hilo independiente**.

### 🔸 `Pipeline`
* Protege las variables compartidas con `threading.Lock()` (Semáforo).
* **Evita condiciones de carrera** al acceder al *frame* de la cámara.
* Contiene la lógica de **YOLO + Segmentación**.

---

## 5️⃣ Dashboard en Streamlit

La interfaz de usuario implementada:
* Muestra las **detecciones en tiempo real**.
* Muestra la **máscara de segmentación**.
* Muestra el **FPS** (Frames por Segundo) aproximado.
* **No se bloquea** gracias al pipeline multihilo.

---

## 6️⃣ Dockerización

Se preparó la aplicación para un despliegue portable:

### 🛠 Configuración de Docker
* `Dockerfile` con imagen base **Python 3.11** (o la versión que hayas usado).
* Instalación de **OpenCV**, **ultralytics**, y demás librerías en un entorno aislado.
* **Exposición** del dashboard en el puerto **8501**.

### ⚙ Comandos de Docker (Pendientes de añadir)

```bash
docker build -t segmentacion 
docker run -p 8501:8501 segmentacion
```

| Problema | Causa | Solución |
| :--- | :--- | :--- |
| **Roboflow no descarga .pt** | Requiere plan pago | **Entrenar gratis en Google Colab** |
| **MediaPipe daba máscaras blancas** | No segmenta objetos electrónicos | **Reemplazar por segmentación basada en YOLO** |
| **`ModuleNotFoundError: src`** | Dashboard se ejecutaba desde carpeta incorrecta | **Agregar `sys.path.append(BASE_DIR)`** |
| **No encontraba modelo YOLO** | Carpeta equivocada (`models` vs `model`) | **Establecer estructura fija y corregir rutas** |
| **Streamlit no mostraba nada** | Bloqueo por captura de cámara | **`Thread` dedicado para cámara** |
| **Segmentación invisible** | MediaPipe devolvía fondo plano | **Cambiar a segmentador simple** |

# 🧠 Conclusión del Punto 2

Este punto del taller permitió construir un **sistema completo de detección y segmentación** aplicando los siguientes pilares tecnológicos:

* **Visión por computadora**
* Entrenamiento de **modelos YOLO**
* **Concurrencia** mediante **hilos**
* **Sincronización** con `locks` (Semáforos)
* Despliegue profesional en **Docker**
* Interfaz interactiva en **Streamlit**

---

A pesar de las **dificultades técnicas** —como incompatibilidades con MediaPipe, problemas con rutas, modelos no compatibles y restricciones de Roboflow— se logró un sistema bastante **funcional**, y capaz de ejecutarse en **tiempo real**.
