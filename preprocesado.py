from stopwords import stopwords

def minusculas(linea):
    """Esta función toma una linea de texto (string) y transforma todos los
    carácteres a minúsculas (regresa un string)

    """
    nueva_linea = linea.lower()
    return nueva_linea

def limpiar_linea(linea):
    """Esta función acepta una línea de texto (str) y regresa un nuevo string
    sin caracteres especiales (.,?!*/).
    El módulo string de la librería estándar de python contiene estos
    caracteres si los desean. Los incluyo al principio de su código.

    """
    from string import punctuation #Esta cosa tiene los signos de puntuacion
    #Ira agregando caracteres si estos no son algunos de los que estan en punctuation
    linea_limpia = "".join(caracter for caracter in linea if caracter not in punctuation)
    return linea_limpia

def obtener_tokens(linea):
    """Esta función recibe una línea de texto y la transforma en una lista
    cuyos elementos son las palabras en la linea.

    """
    nueva_linea = linea.split()
    return nueva_linea

def limpiar_tokens(tokens, stopwords):
    """Esta función recibe una lista de palabras (tokens) y elimina aquellas
    que se encuentren en la lista de stopwords (regresa lista de palabras sin
    stopwords).

    """
    tokens_limpios = [caracter for caracter in tokens if caracter not in stopwords]
    return tokens_limpios

def preprocesar_linea(linea):
    """Esta función aplica las funciones anteriores a una línea de texto
    (string). Debe regresar tokens limpios (lista de strings).

    """
    linea_preprocesada = minusculas(linea)
    linea_preprocesada = limpiar_linea(linea_preprocesada)
    linea_preprocesada = obtener_tokens(linea_preprocesada)
    linea_preprocesada = limpiar_tokens(linea_preprocesada, stopwords)
    return linea_preprocesada

def preprocesar_libro(libro):
    """Aplica preprocesar_linea a cada linea de un libro. El libro consiste en
    una lista, donde cada elemento es una linea del libro.

    Debe regresar una lista de listas. Las listas interiores son los tokens
    limpios de cada línea.
    """
    #Inicializamos el libro preprocesado en lista vacia
    libro_preprocesado = []
    #Por cada elemento de la lista aplicamos el preprocesado
    for linea in libro:
        libro_preprocesado.append(preprocesar_linea(linea))
    #Esto es para limpiar las listas vacias
    libro_preprocesado = [linea for linea in libro_preprocesado if linea]
    return libro_preprocesado

def leer_libro(filename):
    """Dado el nombre de un archivo, debe leer línea a línea agregandolas a una
    lista, es decir, debe regresar una lista cuyos elementos son las líneas.
    """
    #Inicializamos el libro en lista vacia
    libro = []
    #Abrimos el archivo, la r es para modo lectura
    with open("./Books/" + filename, "r", encoding = "utf-8") as archivo:
        for linea in archivo:
            libro.append(linea.strip())
    return libro

def eliminar_repetidos(libro_preprocesado):
    #Inicializamos las palabras que no estaran repetidas en lista vacia
    palabras = []
    #Por cada elemento de la lista de listas 
    for linea in libro_preprocesado:
        palabras.extend(linea) #El extend es para agregar elementos sueltos a la lista y no la lista entera
    #Primero transformamos en un conjunto el cual no acepta repetidos para luego regresarlo nuevamente a una lista
    return list(set(palabras)) 

#Pruebas
if __name__ == '__main__':
    linea = "Next day the flames had disappeared, and the French officers"
    print(preprocesar_linea(linea))

    filename = "Moby Dick Or The Whale by Herman Melville 4528.txt"
    libro = leer_libro(filename)
    libro = preprocesar_libro(libro)
    print(eliminar_repetidos(libro))