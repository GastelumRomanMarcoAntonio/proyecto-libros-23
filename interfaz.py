# Eres libre de usar tu imaginación aquí
# Imprime aquí mensajes en pantalla que guien a un usuario a usar tu sistema de
# recomendaciones.

# En este archivo debes mandar llamar a los dos módulos:
#    libros y recomendaciones
# ya que los necesitaras para darle respuestas al usuario.

# Debes darle un mensaje al usuario con respecto a lo que hace tu programa.
# Debes preguntar si desea un resumen de palabras de un libro o si desea
# recomendaciones de libros en base a un libro que le haya gustado.
# Debes mostrar una lista con índices y nombres de los libros.

# Si desea un resumen debes preguntarle de qué libro (que te de el índice
# correspondiente) y cuantas palabras desea y despues imprimir la información
# con un formato bonito.

# Si desea recomendaciones de libro: pregúntale que libro le gusta (que te de
# un índice de acuerdo a la lista que le presentaste) y despues le preguntas
# cuantos libros quiere que le recomiendes. Posteriormente, le muestras los
# nombres de los libros recomendados con un buen formato.

import get_books
import libros
import recomendaciones
from string import punctuation

carpeta_destino = "Books/"

def descargar_libros():
    """ Opcion [1]: Funcion exclusiva para descargar libros del top de Gutenberg """
    print("--- Bienvenido al panel de descarga de libros ---")
    while True:
        try:
            cantidad_libros = int(input("Cantidad de libros a descargar: ").strip())
            if cantidad_libros <= 0:
                print("Porfavor introduzca un numero mayor a cero.")
                continue
            break
        except ValueError:
            print("Entrada invalida, porfavor introduzca un numero entero.")

    print(f"\nIniciando la descarga de {cantidad_libros} libros...")
    rango_libro = range(1, cantidad_libros + 1)
    # Llamamos la funcion que descarga los libros del archivo get_books
    get_books.main(n = rango_libro, directory = carpeta_destino)
    print("=" * 31)
    print(" Descarga finalizada con exito ")
    print(f"     {cantidad_libros} libros descargados ")
    print("=" * 31)
    input("\nPresione ENTER para regresar al menu principal...")

def actualizar_motor():
    """ Escanea la carpeta donde estan los libros y calcula de matriz de pesos"""
    # Creamos la lista donde estaran los libros descargados
    lista_libros = libros.crear_lista_libros_ingles(directory = carpeta_destino, caract_especiales = punctuation)
    # Si no hay libros descargados pues regresa nada y una lista vacia
    if not lista_libros:
        return None, []
    # Si si hay libros descargados:
    # Inicializamos el recomendador y calculamos sus pesos
    motor = recomendaciones.Recomendador(lista_libros)
    motor.set_pesos()
    # Regresamos la lista de libros y el motor actualizado
    return motor, lista_libros

def capturar_indice_valido(lista_libros):
    """ Funcion auxiliar para validar que el usuario ingrese un indice correcto """
    try:
        idx = int(input("\nIntroduzca el numero de indice del libro: ").strip())
        if idx < 0 or idx >= len(lista_libros):
            print(f"Indice fuera de rango. Porfavor seleccione un indice entre 0 y {len(lista_libros)-1}.")
            input("\nPresione ENTER para continuar...")
            return None
        return idx
    # Si el usuario no ingresa un numero entero entonces lo manda hacia aca
    except ValueError:
        print("Entrada invalida. Porfavor ingrese un numero entero.")
        input("\nPresione ENTER para continuar...")
        return None

def solicitar_resumen(motor, lista_libros):
    """ Opcion [2]: Pide el indice, la cantidad de palabras y muestra un resumen de las palabras con mayor peso """
    idx = capturar_indice_valido(lista_libros)
    if idx is None: # Utilizamos el "is" para evaluar identidad no un valor
        return  # Si el indice fue invalido, regresamos al menu

    print(f"\nLibro seleccionado: {lista_libros[idx].name}")
    try:
        cantitad_palabras = int(input("Cantidad de palabras que desea ver: ").strip())
        if cantitad_palabras <= 0:
            print("La cantidad debe ser mayor a cero.")
            input("\nPresione ENTER para continuar...")
            return

        # Llamamos al metodo resumen del archivo de recomendaciones.py
        top_palabras = motor.resumen(idx_libro = idx, num_palabras = cantitad_palabras)
        # Mostramos en pantalla el resumen
        print("\n" + "=" * 50)
        print(f" Nombre del libro: {lista_libros[idx].name}")
        print(" " + "-" * 45)
        print(f" Palabras clave: {', '.join(top_palabras)}")
        print("=" * 50)

    except ValueError:
        print("Porfavor ingrese un numero entero.")
    
    input("\nPresione ENTER para regresar al menu principal...")

def solicitar_recomendaciones(motor, lista_libros):
    """Opcion [3]: Pide el libro base, la cantidad deseada y muestra las sugerencias similares """
    if len(lista_libros) < 2: # Verificamos que haya al menos 2 libros para poder buscar parecidos
        print("Se necesitan al menos 2 libros en la biblioteca para buscar parecidos.")
        input("\nPresione ENTER para continuar...")
        return

    idx = capturar_indice_valido(lista_libros) 
    if idx is None: # Utilizamos el "is" para evaluar identidad no un valor
        return # Si el indice fue invalido, regresamos al menu

    print(f"\nLibro seleccionado: {lista_libros[idx].name}")
    try:
        limite_sugerencias = len(lista_libros) - 1
        cantidad_sugerencias = int(input(f"¿Cuantos libros recomendados desea? (Maximo {len(lista_libros)-1}): ").strip())
        if cantidad_sugerencias <= 0: # Validamos que pida al menos una sugerencia
            print("La cantidad debe ser mayor a cero.")
            input("\nPresione ENTER para continuar...")
            return
        # Esto es para que el usuario no pida mas sugerencias que los libros que hay descargados
        if cantidad_sugerencias > limite_sugerencias:
            print(f"No puedes pedir tantas recomendaciones. Solo hay {limite_sugerencias} libros disponibles para comparar.")
            input("\nPresione ENTER para continuar...")
            return

        # Llamamos al metodo libros_similares del archivo de recomendaciones.py
        sugerencias = motor.libros_similares(idx_libro = idx, num_libros = cantidad_sugerencias)
        # Mostramos en pantalla las recomendaciones
        print("\n" + "=" * 50)
        print(f" PORQUE TE GUSTO: {lista_libros[idx].name}")
        print(" Te recomendamos leer:")
        print(" " + "-" * 45)
        for i, nombre in enumerate(sugerencias, start=1):
            print(f"  {i}. {nombre}")
        print("=" * 50)

    except ValueError:
        print("Porfavor ingrese un numero entero.")

    input("\nPresione ENTER para regresar al menu principal...")

def bienvenida():
    """ Funcion exclusivamente para dar una bienvenida """
    print("=" * 46)
    print(" Bienvenido al sistema recomendador de libros")
    print("\n Este programa analiza textos y para extraer")
    print("  conceptos claves y asi poder recomendarte")
    print("             libros similares")
    print("=" * 46)

def menu():
    """ Funcion que hara de menu principal y que llamara a todas las otras funciones """
    # Inicializamos la opcion como 0
    opcion = "0"
    # Inicializamos el motor y obtenemos la lista de los libros
    motor, lista_libros = actualizar_motor()
    # Creamos un bucle infinito hasta que se seleccione la opcion de salir
    while opcion != "4":
        print("\n===========================================")
        print("            MENU DE OPCIONES")
        print("===========================================")
        # Si hay libros descargados entonces los mostramos 
        # mediante el metodo mostrar_libros del archivo recomendaciones.py
        if lista_libros:
            motor.mostrar_libros()
        else: # Si no hay libros descargados, le sugerimos que los descargue mediante la opcion 1
            print("No hay libros descargados, puede empezar descargando utilizando la opcion [1]")
            print("-" * 50)
        # Menu de lo que puede hacer el usuario
        print(" ¿Que es lo que desea hacer?")
        print(" [1] Descargar libros del top de Project Gutenberg")
        print(" [2] Solicitar resumen de palabras clave de un libro")
        print(" [3] Solicitar recomendaciones basadas en un libro")
        print(" [4] Salir del sistema")
        # Pedimos la opcion a ejecutar
        opcion = input("\nSeleccione una opcion (1-4): ").strip()

        if opcion == "1": # Descarga los libros
            descargar_libros() # Llamamos a la funcion que descarga los libros
            print("\nProcesando nuevos textos y recalculando matriz TF-IDF...") 
            motor, lista_libros = actualizar_motor() # Actualizamos la matriz y la lista
            if lista_libros: # Si la lista no esta vacia pues todo fue un exito
                print("¡Motor y lista actualizado con exito!")

        elif opcion == "2": # Muestra un resumen de las palabras con mayor peso
            if not lista_libros:
                print("No hay libros descargados. Debe descargar los libros con la opcion [1] primero.")
                input("\nPresione ENTER para continuar...")
            else:
                motor.mostrar_libros() # Mostramos la lista de libros disponibles
                # Llamamos la funcion que nos dara el resumen
                solicitar_resumen(motor, lista_libros) 

        elif opcion == "3":
            if not lista_libros:
                print("No hay libros descargados. Debe descargar los libros con la opcion [1] primero.")
                input("\nPresione ENTER para continuar...")
            else:
                motor.mostrar_libros() # Mostramos la lista de libros disponibles
                # Llamamos la funcion que nos dara las recomendaciones
                solicitar_recomendaciones(motor, lista_libros)

        elif opcion == "4": # Sale del programa
            print("\n¡Gracias por usar el recomendador! Hasta luego.")
            print("=== Recomendador hecho por: ===")
            print("- Aragon Nava Armando Emmanuel")
            print("- Gastelum Roman Marco Antonio")
            print("- Leon Quiroa Axel Dahil")
            print("- Rubio Amarillas Vianca Nohemi")
            print("- Reyes Salazar Adilene")

        else: # Caso default por si no selecciona una opcion del rango
            print("Opcion invalida. Porfavor elija un numero del 1 al 4.")
            input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    bienvenida()
    menu()