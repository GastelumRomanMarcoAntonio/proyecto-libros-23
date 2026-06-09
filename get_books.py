import os
import requests
from bs4 import BeautifulSoup

def get_links(n: int | list[int] = -1) -> tuple[ list[str], list[str] ]:
    """Obtiene los urls y los nombres de los libros del proyecto de Gutenberg
    deseados.

    Los libros se encuentran en formato txt bajo la sección descargados
    frecuentemente en:
        https://www.gutenberg.org/browse/scores/top.

    Los números `n` deben corresponder a los números en esta lista (empezando
    con uno).

    Parameters
    ----------
    n : int | list[int], optional
        Un entero o lista de enteros con los números de libros deseados.
        Escoge -1 (default) si se desean todos los libros.

    Returns
    -------
    links : list[str]
        Ligas a los archivos txt de los libros.
    titles : list[str]
        Títulos de los libros.
    """
    # URL para los libros
    url = "https://www.gutenberg.org/browse/scores/top"
    # Inicializamos lo que debe regresar la funcion
    links = [] 
    titles = []
    # Coso para que no nos bloquee el navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status()
        # Parsear
        parser = BeautifulSoup(response.text, 'html.parser')
        # Buscamos todas las etiquetas <a>
        etiquetas = parser.find_all("a")
        contador_libros_validos = 0
        if isinstance(n, (list, range)):
            n = set(n)
        # Creamos un conjunto para guardar ids y que estas no se repitan
        ids_vistos = set()
        for enlace in etiquetas:
            direccion_libro = enlace.get("href", "")
            # Filtramos el contenenido para que solo sea de esa pagina
            if direccion_libro.startswith("/ebooks/"):
                book_id = direccion_libro.split("/")[-1]
                # Solo contamos el libro si confirmamos que tiene un ID numerico y la id no ha sido vista
                if book_id.isdigit() and book_id not in ids_vistos:
                    ids_vistos.add(book_id)  # Guardamos el ID para no volverlo a contar
                    contador_libros_validos += 1 # Aumentamos el contador de libros validos
                    # Esto es para saber cuantos libros descargar, es decir si es -1 los descarga todos y si pone otro numero pues esos descarga (rangos tambien), ojito ahi
                    if n == -1 or (isinstance(n, int) and contador_libros_validos <= n) or (isinstance(n, set) and contador_libros_validos in n):   
                        # Generamos el URL necesario para la descarga
                        txt_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
                        # Guardamos el titulo del libro
                        titulo_libro = enlace.get_text(strip = True)
                        # Eliminar caracteres especiales de los titulos
                        titulo_limpio = "".join(caracter for caracter in titulo_libro if caracter.isalnum() or caracter in "._- ").rstrip()
                        titulo_libro = f"{titulo_limpio[:50]}.txt"  
                        links.append(txt_url)
                        titles.append(titulo_libro)

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")
        
    return links, titles

def download_file(url, name, directory):
    """Guarda un archivo que se encuentra en un `url` bajo el nombre que demos
    en `name` en el directorio deseado.
    """
    # Crear el directorio si no existe
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    ruta_completa = os.path.join(directory, name)
    
    try:
        # Direccion principal
        response = requests.get(url, stream=True)
        
        # Esto es por si falla la primera URL
        if response.status_code == 404:
            #Obtenemos el ID del libro directamente desde la URL
            book_id = url.split("/")[-2] 
            
            # Creamos una URL de respaldo (es como el de la primera funcion)
            url_respaldo = f"https://gutenberg.org{book_id}/{book_id}-0.txt"
            
            # Reintentamos la petición con la nueva dirección
            response = requests.get(url_respaldo, stream=True)
            
        # Si ambos intentos fallan, este coso dara error para asi poder ir al except
        response.raise_for_status() 
        
        # Si la descarga es exitosa, guardamos el archivo por fragmentos
        with open(ruta_completa, mode='wb') as file:
            for chunk in response.iter_content(chunk_size=10 * 1024):  # 10kb chunks
                file.write(chunk)
        print(f"Downloaded file: {ruta_completa}")
        
    except requests.exceptions.RequestException:
        print(f"No se pudo descargar en ningún formato: {name}")

def store_files(links, names, directory='./'):
    """Guarda cada liga de la lista de ligas `links` en la computadora
    utilizando el directorio deseado y cada uno de los nombres en names.
    """
    for url, name in zip(links, names):
        download_file(url, name, directory)

def main(n = -1, directory='./'):
    links, titles = get_links(n)
    store_files(links, titles, directory)
    print("Done")

if __name__ == '__main__':
    directory = 'Books/'
    n = range(1) # Esto se puede modificar si queremos, es la cantidad de libros a descargar (tambien puede ser rangos)
    main(n, directory)