from matriz import Matriz
from funciones import *
from aux import safe_input, to_subscript

if __name__ == "__main__":
  print("--- LINAL CLI ---\n")
  print("Esta aplicacion es la version CLI (Command Line Interface)")
  print("Tiene diversas aplicaciones y funciones, que en un futuro se conectaran a una interfaz grafica.\n")

  print("--- CALCULADORA DE SISTEMA DE ECUACIONES ---")
  # Conseguimos la cantidad de incognitas y ecuaciones
  incognitas: int = safe_input("Ingrese la cantidad de incognitas: ", funcion=int)
  ecuaciones: int = safe_input("Ingrese la cantidad de ecuaciones: ", funcion=int)
  # Nuestra cantidad de columnas va a ser nuestras incognitas + 1 (para los resultados)
  # Nuestra cantidad de filas es la cantidad de ecuaciones
  matriz: Matriz = Matriz(ecuaciones, incognitas + 1)
  # Vamos a ciclar para obtener la matriz
  for fila in range(1, ecuaciones + 1):
    print(f"\n-- Fila #{fila} --\n")
    for columna in range(1, incognitas + 2):
      prompt: str = to_subscript(f"Ingrese el coeficiente de X{columna}: ") if columna != incognitas + 1 else "Ingrese el resultado: "
      valor: float = safe_input(prompt, funcion=float)
      matriz.set(fila, columna, valor)
  # Imprimimos la matriz inicial
  print(f"Matriz Inicial:\n{matriz}")
  print("\n\n")
  # Corremos la formula escalonada reducida para todas las columnas y filas menos la del resultado
  resolver_sistema(matriz, ecuaciones, incognitas) 