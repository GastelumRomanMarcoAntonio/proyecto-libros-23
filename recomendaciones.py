import math

class Recomendador:
    def __init__(self, libros) -> None:
        """
        libros: lista con instancias de tipo `Libro`
        """
        self.libros = libros
        self._pesos = None  # Se calcularan con un setter (ver `set_pesos`)

    def set_pesos(self) -> None:
        """Calcula los pesos del algorítmo TF-IDF requeridos para las
        recomendaciones y los guarda en `self._pesos`

        """
        # Obtenemos las frecuencias de palabras de cada libro
        # Preprocesamos todos los libros lo que debe de regresar una lista de diccionarios con sus frecuencias
        frecuencias_libros = [libro.preprocesar_libro() for libro in self.libros]
        cantidad_documentos = len(self.libros) #Cuenta cuantos libros son en total

        # Contar en cuantos libros aparece cada palabra (Document Frequency)
        # Inicializamos el conteo en diccionario vacio
        conteo_documentos_por_palabra = {}
        for diccionario in frecuencias_libros:
            for palabra in diccionario.keys():
                #Esto cuenta cuantas veces aparece una palabra en distintos libros (documentos si lo quieres ver asi)
                conteo_documentos_por_palabra[palabra] = (conteo_documentos_por_palabra.get(palabra, 0) + 1)

        # Calcular la matriz de pesos finales TF-IDF
        # Inicializamos los pesos como lista vacia
        self._pesos = []
        for diccionario in frecuencias_libros:
            pesos_libro = {} # Inicializamos los pesos de los libros como diccionario vacio
            # Buscamos la frecuencia de la palabra mas comun en este libro para normalizar el TF
            max_tf = max(diccionario.values()) if diccionario else 1
            # Calculamos el TF e IDF
            for palabra, tf in diccionario.items():
                # TF normalizado: cuantas veces sale la palabra entre el máximo de este libro
                tf_normalizado = tf / max_tf
                # IDF: que tan rara o comun es la palabra en toda la biblioteca
                df = conteo_documentos_por_palabra[palabra]
                idf = math.log10(cantidad_documentos / df)
                # El peso final es la multiplicacion de ambos componentes
                pesos_libro[palabra] = tf_normalizado * idf
            # Se van añadiendo los pesos a la lista de pesos
            self._pesos.append(pesos_libro)

    def get_pesos(self):
        """Regresa los pesos calculados"""
        return self._pesos

    def _producto_punto(self, idx_1:int, idx_2:int) -> float:
        """Producto punto entre los libros con índices idx_1 y idx_2."""
        # Extraemos los diccionarios de pesos de los dos libros a comparar
        pesos_libro1 = self._pesos[idx_1]
        pesos_libro2 = self._pesos[idx_2]
        # Inicializamos una variable acumuladora
        resultado = 0.0
        # Iteramos sobre las palabras del primer libro
        for palabra, peso1 in pesos_libro1.items():
            # Si la palabra tambien existe en el segundo libro multiplicamos sus pesos
            if palabra in pesos_libro2:
                peso2 = pesos_libro2[palabra]
                resultado += peso1 * peso2

        return resultado

    def _similitud(self, idx_1, idx_2) -> float:
        """Similitud entre los libros con índices idx_1 y idx_2 de acuerdo al
        coseno del ángulo que forman sus vectores.

        """
        # Si el libro que estamos comparando es el mismo libro pues la similitud es del 100%
        if idx_1 == idx_2:
            return 1.0

        # Obtenemos el producto punto 
        prod_punto = self._producto_punto(idx_1, idx_2)
        # Calculamos la norma (magnitud) del vector del libro 1
        # Sumamos los cuadrados de todos sus pesos y sacamos raiz cuadrada
        norma_libro1 = math.sqrt(sum(peso**2 for peso in self._pesos[idx_1].values()))
        # Calculamos la norma (magnitud) del vector del libro 2
        norma_libro2 = math.sqrt(sum(peso**2 for peso in self._pesos[idx_2].values()))
        # Si alguna norma es cero evitamos la division por cero para que no de error
        if norma_libro1 == 0 or norma_libro2 == 0:
            return 0.0
        
        # Usamos la formula del coseno
        return prod_punto / (norma_libro1 * norma_libro2)

    def mostrar_libros(self):
        """Mostrarle al usuario el índice y nombre para cada libro de acuerdo a
        nuestra lista de libros `self.libros`.

        """
        print("\n--- Catalogo de libros en la biblioteca ---")
        # Usamos el enumerate para que nos de los indice automaticamente
        for idx, libro in enumerate(self.libros):
            # Mostramos el indice y el nombre del libro
            print(f" Indice [{idx}]: {libro.name}")
        print("-" * 43) # Puro diseño nada mas

    def resumen(self, idx_libro, num_palabras) -> list[str]:
        """Regresa una lista con las palabras más representativas de un libro
        de acuerdo a los pesos.

        idx_libro: índice del libro cuyo resumen deseamos.
        num_palabras: número de palabras en el resumen.

        """
        # Extraemos el diccionario de pesos TF-IDF para el libro solicitado
        pesos_libro = self._pesos[idx_libro]

        # Ordenamos las palabras de mayor a menor basandonos en su peso
        # x[1] representa el peso TF-IDF en la tupla (palabra, peso)
        # Por ejemplo: [('whale', 0.67)] el [1] seria 0.67 que es el peso el indice 1
        palabras_ordenadas = sorted(pesos_libro.items(), key=lambda x: x[1], reverse=True)

        # Extraemos unicamente las palabras del top solicitado mediante un desempaquetado
        # La variable peso esta solamente como auxiliar para poder hacer el desempaquetado
        top_palabras = [palabra for palabra, peso in palabras_ordenadas[:num_palabras]]

        return top_palabras

    def libros_similares(self, idx_libro, num_libros) -> list[str]:
        """Regresa una lista con los libros más parecidos a un libro dado.

        idx_libro: índice del libro a partir del cual quiero recomendaciones.
        num_libros: número de libros en mi recomendación.


        """
        # Inicializamos la lista de los libros similares como lista vacia
        lista_similitudes = []
        # Calculamos la similitud del libro base contra todos los libros de la biblioteca
        for idx_otro, libro_otro in enumerate(self.libros):
            # Saltamos la comparacion si es el mismo libro
            if idx_otro == idx_libro:
                continue

            # Invocamos el metodo de similitud de coseno
            valor_similitud = self._similitud(idx_libro, idx_otro)
            
            # Guardamos la informacion en una tupla: (nombre_del_libro, valor_matematico)
            # Y se agrega a la lista de similitudes
            lista_similitudes.append((libro_otro.name, valor_similitud))

        # Ordenamos la lista de mayor a menor basandonos en el valor de similitud (el indice 1 de la tupla)
        lista_ordenada = sorted(
            lista_similitudes, key=lambda x: x[1], reverse=True
        )

        # Recortamos la lista para regresar solo el número de recomendaciones solicitado
        # Extraemos únicamente el nombre del libro (el indice 0 de la tupla)
        # num_libros es la cantidad de libros a tomar
        top_recomendaciones = [nombre for nombre, similitud in lista_ordenada[:num_libros]]

        return top_recomendaciones