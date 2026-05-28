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
    #URL para los libros
    url = "https://www.gutenberg.org/browse/scores/top"
    #Inicializamos lo que debe regresar la funcion
    links = [] 
    titles = []
    #Coso para que no nos bloquee el navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        #Parsear
        parser = BeautifulSoup(response.text, 'html.parser')
        #Buscamos todas las etiquetas <a>
        etiquetas = parser.find_all("a")
        contador_libros_validos = 0
        for enlace in etiquetas:
            direccion_libro = enlace.get("href", "")
            #Filtramos el contenenido para que solo sea de esa pagina
            if direccion_libro.startswith("/ebooks/"):
                book_id = direccion_libro.split("/")[-1]
                #Descartamos enlaces o secciones que no terminen en un ID numerico
                if book_id.isdigit():
                    contador_libros_validos += 1
                    # Comprobamos las condiciones del parámetro 'n' basados en el ranking real
                    if n == -1 or (isinstance(n, int) and contador_libros_validos <= n) or (isinstance(n, list) and contador_libros_validos in n):
                        txt_url = f"https://gutenberg.org{book_id}.txt.utf-8"
                        titulo_libro = enlace.get_text(strip=True)
                        links.append(txt_url)
                        titles.append(titulo_libro)

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")
        
    return links, titles

#Pruebas
link, titulos = get_links(50) #El parametro es la cantidad de libros a buscar ojito ahi

print(f"Cantidad de libros obtenidos: {len(link)}\n")
for i, (titulo, link) in enumerate(zip(titulos, link), start=1):
    print(f"{i}. {titulo}")
    print(f"   Enlace: {link}")