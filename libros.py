from pathlib import Path
from string import punctuation
from nltk.corpus import stopwords


class Libro:
    def __init__(self, name, filename) -> None:
        """Crear atributos públicos """
        self.name = name
        self.filename = filename
        self.CARACTERES_ESPECIALES: str | None = None
        self.STOPWORDS: list[str] | None = None
        # hacer que estos atributos sean de tipo property (al setter hay que
        # incluirle validación)
        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, value):
            """Checar que el nombre sea un string"""
            if not isinstance(value, str):
                raise TypeError("El nombre del libro debe ser un string")
            self._name = value

        @property
        def filename(self):
            return self._filename
        
        @filename.setter
        def filename(self, value):
        #     """Checar que el nombre sea un string y que el archivo existe"""
            archivo = Path(value)
            if not isinstance(value, str): #Si no es un string mandamos un error de tipo
                raise TypeError("El nombre del archivo debe ser un string")
            if not archivo.exists(): #Si no existe el archivo mandamos un error de no encontrado
                raise FileNotFoundError("El archivo no existe") 
            self._filename = value

    def _limpiar_linea(self, linea):
        """Este método toma una línea de texto (str) y elimina los caracteres
        en `self.CARACTERES_ESPECIALES`.

        """
        linea_limpia = "".join(caracter for caracter in linea if caracter not in self.CARACTERES_ESPECIALES)
        return linea_limpia

    def _limpiar_tokens(self, tokens):
        """Este método recibe una lista de palabras (`tokens`) y elimina
        aquellas que se encuentran en `self.STOPWORDS` modificando la lista
        original. (regresa lista de palabras sin stopwords)

        """
        #Usamos el [:] para modificar la lista original internamente
        tokens[:] = [token for token in tokens if token not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea) -> list[str]:
        """Limpia una línea de texto regresando tokens  limpios. La limpieza
        debe considerar eliminar espacios blancos al principio y final de la
        línea, convertir a minúsculas, eliminar caracteres especiales, crear
        tokens y eliminar stopwords en estos tokens.

        Este método debe aplicar los métodos anteriores donde sea necesario.
        Debe regresar tokens limpios (lista de strings).

        """
        # eliminar espacios blancos al principio y final de la línea
        linea_limpia = linea.strip()
        # convierte la linea a minúsculas
        linea_limpia = linea_limpia.lower()
        # elimina los caracteres especiales
        linea_limpia = self._limpiar_linea(linea_limpia)
        # obten tokens: transforma la linea en una lista de palabras
        tokens = linea_limpia.split()
        # limpia la lista de tokens
        tokens = self._limpiar_tokens(tokens)
        """Esto filtra los tokens para que solo queden los que tengan más de 1 letra
        Esto porque en algunos libros las palabras mas comunes eran "n", "v", "a", etc etc"""
        tokens = [token for token in tokens if len(token) > 1]
        return tokens

    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista, es decir, debe regresar una lista cuyos
        elementos son las líneas no vacías del libro (el primer elemento es la
        primer línea no vacía y así sucesivamente).

        """
        #Inicializamos el libro en lista vacia
        libro = []
        #Abrimos el archivo, la r es para modo lectura
        with open("./Books/" + self.filename, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                #Si la linea no esta vacia pues la agregamos a la lista
                if linea_limpia:
                    libro.append(linea_limpia)
        return libro

    def preprocesar_libro(self) -> dict[str, int]:
        """Regresa un diccionario de palabras relevantes del libro como llaves
        (los tokens limpios) y sus respectivas frecuencias como valores. Por
        ejemplo, puede regresar:
            {'shrek': 55, 'fiona': 43, 'caminando': 8}

        Para hacer esto, aplica `preprocesar_linea` a cada linea del `libro`
        agregando cada token limpio con un valor de 1 al diccionario si la
        palabra no existe o aumentado el contador de la palabra correspondiente
        en caso contrario.

        """
        #Inicializamos las frecuencias como un diccionario vacio
        frecuencias = {}
        #Obtenemos las lineas del libro
        lineas_libro = self.leer_libro()
        #Aplicamos el preprocesar linea a cada linea del libro
        for linea in lineas_libro:
            tokens_limpios = self._preprocesar_linea(linea)
            #Se suman las frecuencias al diccionario
            for token in tokens_limpios:
                frecuencias[token] = frecuencias.get(token, 0) + 1      
        return frecuencias

    def __str__(self) -> str:
        """Regresa la representación de este objeto en forma de un string.

        Esta es una representación informal que tiene como objetivo que el
        objeto sea entendible para el usuario cuando utilizamos `print` (esta
        función se ejecuta cuando utilizamos ese comando).

        Ver archivo: `Codes/clase_grupo.py` para un ejemplo.

        O bien puedes ver:
          https://realpython.com/python-classes/#special-methods-and-protocols

        """
        return f"Nombre del libro: {self.name}\nNombre y ruta del archivo: {self.filename}"

    def __repr__(self) -> str:
        """Regresa la representación formal del objeto.

        En esta función regresamos un string que tome la forma en la que
        creariamos esta instancia.

        Ver archivo: `Codes/clase_grupo.py` para un ejemplo.

        O bien puedes ver:
          https://realpython.com/python-classes/#special-methods-and-protocols

        """
        #El !r sirve para que el texto aparezca con comillas
        #Fuerza la representación tecnica (repr) para que el texto conserve sus comillas
        return f"name = {self.name!r}, filename = {self.filename!r}"

# Los libros del proyecto Gutenberg empiezan dando información sobre el
# copyright y los créditos. El contenido se encuentra después de una línea que
# inicia con `*** START` y antes de la linea `*** END`. Esto debe
# considerarse al momento de leer el libro. Por lo tanto, reescribimos el
# método copprespondiente.
class LibroGutenberg(Libro):
    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista. Además, empieza a agregar solo despues de
        la línea que comienza con `*** START` y antes de la línea `*** END`.

        (Debe regresar una lista cuyos elementos son las líneas no vacías del
        libro que se encuentran entre las líneas `*** START` y `*** END`.)

        """
        #Inicializamos el libro como lista vacia
        libro = []
        #Esto es para saber si ya estamos dentro del contenido libro y no el copyright y los creditos
        #Actuara como una bandera
        es_contenido = False
        #Esto es lo mismo de lo del preprocesado.py
        with open(self.filename, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                #Si encontramos la linea que inicia con "*** START", la bandera se activa
                if linea_limpia.startswith("*** START"):
                    es_contenido = True
                    continue  #Esto es para saltarnos esa linea del "*** START" y siga su camino 
                #Si encontramos la linea que inicia con "*** END", desactivamos la bandera y salimos
                if linea_limpia.startswith("*** END"):
                    es_contenido = False
                    break  #Si ya llegamos al final pues no tiene caso seguir buscando         
                #Solo si la bandera esta activa y la línea no esta vacia, la guardamos
                if es_contenido and linea_limpia:
                    libro.append(linea_limpia)
        return libro

# Los libros en distintos idiomas tienen distintos `STOPWORDS`.
class LibroEnglish(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en ingles (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        self.STOPWORDS = set(stopwords.words('english'))

class LibroSpanish(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en español (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        self.STOPWORDS = set(stopwords.words('spanish'))

class LibroFrench(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en francés (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        self.STOPWORDS = set(stopwords.words('french'))

# La siguiente función asume que todos los libros se encuentran en el
# directorio `directory`, tienen extensión `txt` y todos son en inglés.
def crear_lista_libros_ingles(directory: str, caract_especiales=punctuation):
    """Crea una lista de instancias `LibroEnglish` a partir de libros
    localizados en `directory`.

    No ocupas modificar esta función, se encuentra ya implementada.

    """
    libros = []
    path = Path(directory)
    for file in path.glob('*.txt'):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros

#Pruebas
if __name__ == "__main__":
    mi_libro = Libro("Moby Dick", "./Books/moby.txt")
    print(mi_libro)
    print(repr(mi_libro))