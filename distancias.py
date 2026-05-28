import requests
import urllib.parse


API_KEY = "dfa3ac80-43c0-4f8a-8073-e098b39a1efd"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(ciudad):
 
    url = f"{GEOCODE_URL}q={urllib.parse.quote(ciudad)}&key={API_KEY}"
    respuesta = requests.get(url).json()
    
  
    if respuesta.get("hits") and len(respuesta["hits"]) > 0:
        lat = respuesta["hits"][0]["point"]["lat"]
        lng = respuesta["hits"][0]["point"]["lng"]
        return lat, lng
        
    return None, None

while True:
    print("\n--- Planificador de Rutas ---")
    
    # Solicitar Ciudad de Origen y salida con 'q'
    origen = input("Ingrese la Ciudad de Origen (o presione 'q' para salir): ")
    if origen.lower() == 'q':
        print("Saliendo del programa...")
        break
        
    # Solicitar Ciudad de Destino y salida con 'q'
    destino = input("Ingrese la Ciudad de Destino (o presione 'q' para salir): ")
    if destino.lower() == 'q':
        print("Saliendo del programa...")
        break

    # Obtener coordenadas para ambas ciudades
    lat_origen, lng_origen = obtener_coordenadas(origen)
    lat_destino, lng_destino = obtener_coordenadas(destino)

    if not lat_origen or not lat_destino:
        print("No se pudieron encontrar las coordenadas de una o ambas ciudades. Intente nuevamente.")
        continue

    # Solicitud de la ruta a la API de GraphHopper
    url_ruta = f"{ROUTE_URL}point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&vehicle=car&locale=es&key={API_KEY}"
    respuesta_ruta = requests.get(url_ruta).json()

    if "paths" in respuesta_ruta:
        ruta = respuesta_ruta["paths"][0]
        
        # 1. Medir distancia en kilómetros
        distancia_km = ruta["distance"] / 1000
        
        # 2. Calcular la duración del viaje en horas, minutos y segundos
        tiempo_ms = ruta["time"]
        segundos_totales = tiempo_ms // 1000
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60
        
        # 3. Calcular el combustible requerido en litros
        # Se asume un rendimiento estándar de 12 km por litro para el ejercicio
        rendimiento_km_l = 12.0
        combustible_litros = distancia_km / rendimiento_km_l

        # 4. Imprimir la narrativa del viaje garantizando dos decimales (.2f)
        print("\n--- Narrativa del Viaje ---")
        print(f"Viajando desde {origen.capitalize()} hasta {destino.capitalize()}.")
        print(f"La distancia total es de {distancia_km:.2f} kilómetros.")
        print(f"La duración estimada del viaje es de {horas:02d} horas, {minutos:02d} minutos y {segundos:02d} segundos.")
        print(f"Se requerirán aproximadamente {combustible_litros:.2f} litros de combustible para completar el recorrido.")
    else:
        print("Error al calcular la ruta. Revisa tu token o tu conexión de red.")