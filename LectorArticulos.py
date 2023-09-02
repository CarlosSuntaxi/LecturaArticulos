import requests
from bs4 import BeautifulSoup
import pyttsx3

class LectorArticulos:
    def __init__(self):
        self.voces = self.obtener_voces_disponibles()  # Inicializa una lista de voces disponibles.
        self.idioma_seleccionado = "es-ES"  # Establece el idioma predeterminado como Español (España)

    def obtener_voces_disponibles(self):
        # Inicializa el motor de síntesis de voz.
        engine = pyttsx3.init()
        # Obtiene todas las voces disponibles en el sistema.
        voces = engine.getProperty('voices')
        return voces

    def obtener_contenido(self, url, selector):
        # Realiza una solicitud HTTP a la URL especificada.
        response = requests.get(url)
        # Verifica si la solicitud fue exitosa (código de estado 200).
        if response.status_code == 200:
            # Analiza el contenido HTML de la página web.
            soup = BeautifulSoup(response.text, 'html.parser')
            # Selecciona los elementos HTML con el selector CSS especificado.
            elementos = soup.select(selector)
            # Inicializa el motor de síntesis de voz.
            engine = pyttsx3.init()

            # Configura la voz según el idioma seleccionado.
            for voz in self.voces:
                if self.idioma_seleccionado in voz.id:
                    engine.setProperty('voice', voz.id)
                    break

            # Lee en voz alta el contenido de los elementos seleccionados.
            for i, elemento in enumerate(elementos, start=1):
                print(f"Elemento {i}:")
                print(elemento.text)
                engine.say(elemento.text)
                engine.runAndWait()

                # Verifica si se ha presionado alguna tecla para detener la lectura.
                if input("Presiona cualquier tecla para detener la lectura (o Enter para continuar)..."):
                    break  # Detiene la lectura si se ha presionado una tecla.

        else:
            print("Error al acceder a la página web.")

    def ejecutar(self):
        while True:
            print("Menú:")
            print("1. Leer elementos de una página web")
            print("0. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                url_pagina = input("Ingresa la URL de la página web: ")

                # Sugerencias para el selector CSS simplificadas para niños.
                print("Selecciona qué quieres leer:")
                print("1. Texto normal")
                print("2. Títulos grandes")
                print("3. Encabezado especial")
                seleccion_selector_css = input("Ingresa el número de lo que quieres leer: ")

                opciones_selector_css = {
                    "1": "p",
                    "2": "h1",
                    "3": "div.article"
                }

                selector_elemento = opciones_selector_css.get(seleccion_selector_css)

                if selector_elemento:
                    self.obtener_contenido(url_pagina, selector_elemento)
                else:
                    print("Selección no válida. Por favor, elige una opción válida.")

            elif opcion == "0":
                break
            else:
                print("Opción no válida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    lector = LectorArticulos()  # Crea una instancia de la clase LectorArticulos.
    lector.ejecutar()  # Ejecuta el programa principal.
                
