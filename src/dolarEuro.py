import requests
import json


# Pusimos el calculo aparte por una cuestion higienica

async def dolarfuneu():

# Lista a devolver a euro
    dolarLista = {}

# Llama a la API
    response = requests.get("https://dolarapi.com/v1/dolares")

    # Carga el JSON en Python dictionaro
    json_dolar = json.loads(response.text)          
    preciosdolares = response.json()
    dolares = []

    # Recorre el json y trae los datos para el embed del Euro   
    for casa in preciosdolares:
      nombre = casa["nombre"]
      preciocompra = casa["compra"]
      precioventa = casa["venta"]
      dolar = {"nombre": nombre, "preciocompra": preciocompra, "precioventa": precioventa}
      dolares.append(dolar)

    # Trae precios del Euro en Blue y en Oficial  
    for i in dolares:
       if i['nombre'] == 'Oficial':
          dolarLista[i['nombre']] = i['precioventa']
       elif i['nombre'] == 'Blue':
            dolarLista[i['nombre']] = i['precioventa']
        
    return dolarLista