from matriz import Matriz

# Creamos una matriz de 3 x 3
mat: Matriz = Matriz(filas=3, columnas=3)

mat.set(fila=2, columna=2, valor=3)

# Imprimimos
print(mat)