import preprocesado
import nltk
from nltk.corpus import stopwords

def main(filename: str) -> dict[str, int]:
    # Definir lista con caracteres especiales.
    # Utilizar los caracteres dados por `punctuation` en la librería `string`
    from string import punctuation
    caracteres_especiales = punctuation
    #Definir lista con stopwords
    # Utilizar los stopword en inglés dados en la librería nltk (como vimos en
    # clase).
    # stopwords = ...
    #Descargar los stopwords
    try:
        nltk.data.find('corpora/stopwords') #Busca si ya estan descargados y si lo esta, pues continua normal
    except LookupError:
        nltk.download('stopwords') #Si no estan descargados pues los instala
    stopwords_english = set(stopwords.words('english'))
    stopwords_spanish = set(stopwords.words('spanish'))
    mis_stopwords = stopwords_english | stopwords_spanish #Unimos ambos conjuntos

    # Leer el libro utilizando función correspondiente del módulo `preprocesado`
    libro_lineas = preprocesado.leer_libro(filename)
    # Preprocesar el libro obteniendo un diccionario de palabras relevantes y
    # sus frecuencias y retornar este resultado.
    # Debes utilizar el método correspondiente en `preprocesado`.
    frecuencias = preprocesado.preprocesar_libro(libro_lineas, caracteres_especiales, mis_stopwords)
    return frecuencias

if __name__ == '__main__':
    # Definir a continuación `filename`
    # filename = ...
    filename = "Moby Dick Or The Whale by Herman Melville 4447.txt"
    # Ahora descomenta la línea de abajo
    frecuencias = main(filename)
    for palabra in list(frecuencias.keys())[:200]:
        print(f"{palabra}: {frecuencias[palabra]}")
    # Una vez llenado el módulo preprocesado y este script, puedes ejecutarlo
    # escribiendo en la terminal
    # python procesar_texto