import re
import os
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from parsimonious.grammar import Grammar

def cargar_diccionario(numero):
    nombre_archivo = f"diccionario_espanol ({numero}).txt"
    with open(nombre_archivo, "r", encoding="utf-8") as file:
        return set(word.strip() for word in file.readlines())

def cargar_emoticones():
    return [":)", ":(", ":D", ";)", ":P", "xD", ":-)", ":-(", "(y)", "(n)", "<3", "\\m/", ":-O", ":O", ":-|", ":|", ":*", ">:(", "^^", ":-]", "..."]

def analizador_lexicografico(cadena):
    diccionarios_espanol = [cargar_diccionario(numero) for numero in range(1, 28)]
    emoticones = cargar_emoticones()

    # Expresión regular para identificar palabras en español
    palabras_espanol = re.findall(r'\b[a-zA-Záéíóúüñ]+\b', cadena)

    # Reemplazar emoticones en la cadena
    for i, emoticon in enumerate(emoticones, start=1):
        cadena = cadena.replace(emoticon, f"EMOTICON_{i}")

    # Contar palabras en español y emoticones identificados
    cantidad_palabras_espanol = sum(1 for palabra in palabras_espanol if any(palabra.lower() in diccionario for diccionario in diccionarios_espanol))
    cantidad_emoticones = cadena.count("EMOTICON_")

    return cadena, cantidad_palabras_espanol, cantidad_emoticones

def analizador_sintactico(cadena):
    grammar = Grammar(
        r"""
        cadena = (palabra / emoticon / espacio)+
        palabra = ~"[a-zA-Záéíóúüñ]+"
        emoticon = ~":\)|:\(|:D|;\)|:P|xD|:-\)|:-\(|\(y\)|\(n\)|<3|\\m/|:-O|:O|:-\||:\||:\*|>:\(|\^\^|:-\]"
        espacio = ~"\s+"
        """
    )
    try:
        tree = grammar.parse(cadena)
        return True
    except Exception as e:
        print(f"Error de sintaxis: {e}")
        return False

def mostrar_resultados():
    entrada = entrada_text.get("1.0", tk.END)
    if analizador_sintactico(entrada):
        salida, palabras_espanol, emoticones = analizador_lexicografico(entrada)

        # Mostrar resultados en la GUI
        salida_text.delete("1.0", tk.END)
        salida_text.insert(tk.END, salida)

        resultados_text.config(text=f"Palabras en español: {palabras_espanol}\nEmoticones identificados: {emoticones}")

# Configuración de la GUI
root = tk.Tk()
root.title("Analizador Lexicográfico")

entrada_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
entrada_text.pack(pady=10)

analizar_button = tk.Button(root, text="Analizar", command=mostrar_resultados)
analizar_button.pack(pady=5)

salida_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
salida_text.pack(pady=10)

resultados_text = tk.Label(root, text="")
resultados_text.pack(pady=5)

root.mainloop()
