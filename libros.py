import preprocesado 

class Libro:
    def __init__(self, filename):
        self.filename = filename
        self.lineas = preprocesado.leer_libro(filename)
        #Estos atributos se inicializaran vacios hasta que se llamen los metodos
        self.contenido_preprocesado = []
        self.palabras_unicas = []

    def procesar(self):
        #Se procesa el libro con las funciones del otro archivo
        self.contenido_preprocesado = preprocesado.preprocesar_libro(self.lineas)
        return self.contenido_preprocesado

    def obtener_vocabulario(self):
        """Genera y regresa la lista de palabras únicas del libro."""
        #Si el atributo contenido_preprocesado esta vacio osea false, pues lo procesa automaticamente
        if not self.contenido_preprocesado:
            self.procesar()       
        #Esto guarda las palabras unicas, es decir el vocabulario del libro
        self.palabras_unicas = preprocesado.eliminar_repetidos(self.contenido_preprocesado)
        return self.palabras_unicas

#Pruebas
if __name__ == '__main__':
    mi_libro = Libro("Moby Dick Or The Whale by Herman Melville 4528.txt")
    lineas_limpias = mi_libro.procesar()
    vocabulario = mi_libro.obtener_vocabulario()
    print(vocabulario)
