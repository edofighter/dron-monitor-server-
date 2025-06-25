#Servidor de Monitoreo 🖥️ (Centro de Control)
#librerías necesarias
import socket
import threading
import pandas as pd
import json

#configuracion 
HOST='aqui la ip del hotspot'  #IP hotspot
PORT=65432        # Puerto del servidor

# almacenamiento de datos
datos_drones = []
lock = threading.Lock()
contador = {}

# función para manejar la conexión de cada cliente 
def manejar_cliente(conn, addr, id_drone):
    print(f"[CONECTADO] drone {id_drone} desde {addr}")
    with conn:
        while True:
            try:
                # Recibir datos del drone
                data = conn.recv(1024)
                if not data:
                    break  # Si no hay datos, salir del bucle

                # Decodificar y procesar los datos recibidos
                mensaje = json.loads(data.decode('utf-8'))
                print(f"[RECIBIDO] {mensaje} desde el drone {id_drone}")

                # Almacenar los datos en la lista de drones
                with lock:
                    datos_drones.append(mensaje)
                    contador[id_drone] = contador.get(id_drone, 0) + 1

                    # Crear DataFrame con los datos actuales
                    df = pd.DataFrame(datos_drones)

                    # Mostrar cada 5 datos por dron
                    if contador[id_drone] % 5 == 0:
                        print(f"[DATOS] Drone {id_drone} ha enviado {contador[id_drone]} mensajes.")
                        print(df[df['Dron'] == id_drone].tail(5))  # Mostrar los últimos 5 datos de este dron

                        df.to_csv('datos_drones.csv', index=False)
                        df.to_json('datos_drones.json', orient='records', indent=4)

                        promedio_lat = df[df['Dron'] == id_drone]['Latitud'].mean()
                        promedio_lon = df[df['Dron'] == id_drone]['Longitud'].mean()
                        min_bateria = df[df['Dron'] == id_drone]['Batería'].min()
                        peso_total = df[df['Dron'] == id_drone]['Peso Paquete'].sum()

                        print(f"→ Coordenadas promedio: ({promedio_lat}, {promedio_lon})")
                        print(f"→ Batería mínima: {min_bateria}%")
                        print(f"→ Peso total transportado: {peso_total} kg")

                        # alertas 
                        if min_bateria < 35:
                            print(f" [ALERTA] Batería del drone {id_drone} por debajo del 35%!")
                        if peso_total > 4.5:
                            print(f"  [ALERTA] Peso total transportado por el drone {id_drone} excede los 4.5 kg!")
            except Exception as e:
                print(f"[ERROR] {e}")
                break
            
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[ESCUCHANDO] Servidor en {HOST}:{PORT}")
    id_dron = 1
    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, f'Dron{id_dron}'))
        hilo.start()
        id_dron += 1

if __name__ == "__main__":
    iniciar_servidor()
