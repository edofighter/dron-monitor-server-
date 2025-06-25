# 🛰️ Servidor de Monitoreo de Drones – Centro de Control

Este proyecto implementa un servidor multicliente en Python que permite recibir, almacenar y analizar datos enviados por drones conectados a través de sockets TCP. Está pensado como un centro de control para monitorear en tiempo real ubicación, batería y carga transportada, generando alertas cuando se detectan condiciones críticas.

## 📦 Características

- 🧠 Soporte multicliente (multi-dron) con `threading`
- 📍 Registro de coordenadas GPS (latitud y longitud)
- 🔋 Monitoreo de batería y alertas por bajo nivel (< 35%)
- ⚖️ Control de peso transportado con alertas (> 4.5 kg)
- 📊 Exportación automática a CSV y JSON
- 🔒 Sin bloqueo entre hilos gracias a `threading.Lock()`

## 🚀 Requisitos

- Python 3.7 o superior
- Librerías:
  - `pandas`
  - `socket`
  - `threading`
  - `json`

Instálalas fácilmente con:

```bash
pip install -r requirements.txt
