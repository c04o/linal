from matriz import Matriz
from funciones import *

# Uso de la clase matriz y las funciones
if __name__ == "__main__":
  # Creamos una matriz de 3 x 3
  mat: Matriz = Matriz(filas=3, columnas=4)

  # matriz = [
  #   [1, 1, 1, 6],
  #   [2, 5, 1, -4],
  #   [2, 3, 4, 5]
  # ]

  matriz = [
    [1, 2, -1, 3],
    [2, 4, -2, 6],
    [3, 6, -3, 9]
  ]

  for i in range(0, len(matriz)):
    for j in range(0, len(matriz[i])):
      mat.set(fila=i+1, columna=j+1, valor=matriz[i][j])

  # Imprimimos
  print(mat)
  resolver_gauss_jordan(mat, debug=True)