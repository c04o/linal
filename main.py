from matriz import Matriz
from funciones import *

# Uso de la clase matriz y las funciones
if __name__ == "__main__":
  tamaño: int = 0
  
  # Mientras el usuario no nos de un input valido
  while True:
    # El try catch basicamente agarra errores, entonces, si hay un error convirtiendo el input
    # a numero, pues, atraparemos el error e informaremos al usuario
    try:
      tamaño = int(input("De que tamaño es el sistema de ecuaciones?: "))
      # Si se puede parsear, fin al loop
      break
    except:
      print("Por favor ingrese un número válido")
  
  # Creamos nuestra matriz, con la columna extra para los resultados
  mat: Matriz = Matriz(filas=tamaño, columnas=tamaño + 1)

  for i in range(1, tamaño + 1):
    print(f"Fila #{i}:")
    for j in range(1, tamaño + 2):
      if j == tamaño + 1:
        print(f"Ingrese el valor del resultado: ")
      else:
        print(f"Ingrese el coeficiente de X{j}: ")
      
      valor: float = 0
      # Mientras el usuario no nos de un input valido
      while True:
        # El try catch basicamente agarra errores, entonces, si hay un error convirtiendo el input
        # a numero, pues, atraparemos el error e informaremos al usuario
        try:
          valor = float(input())
          # Si se puede parsear, fin al loop
          break
        except:
          print("Por favor ingrese un número válido")
      
      mat.set(i, j, valor)

  # Imprimimos
  print(f"Matriz:\n{mat}")
  gauss_jordan(mat)