from classes.matriz import Matriz

# Aqui en este archivo van todas las operaciones sobre matrices
# Operaciones basicas en una fila

# Escala una fila por un numero
# a la fila [1][2][3] * 3 -> [3][6][9]
# f -> e*f
def escalar_fila(mat: Matriz, fila: int, escalar: float):
  # Ciclamos por las columnas en la fila
  for i in range(1, mat.columnas + 1):
    nuevo_valor: float = mat.at(fila, i) * escalar
    # En la posicion [fila, i] vamos a cambiar el valor por el mismo pero multiplicado por el escalar
    mat.set(fila, i, nuevo_valor)

# Sumar una fila B a una fila A
# el resultado queda guardado en A
# fa -> fa + fb
def sumar_fila(mat: Matriz, fila_a: int, fila_b: int):
  # Ciclamos de nuevo por las columnas
  for i in range(1, mat.columnas + 1):
    # En la fila A, ponemos el resultado de A + B
    nuevo_valor: float = mat.at(fila_a, i) + mat.at(fila_b, i)
    mat.set(fila_a, i, nuevo_valor)

# Sumar filas escaladas
# fa -> a*fa + b*fb
def sumar_escalar_fila(mat: Matriz, escalar_a: float, fila_a: int, escalar_b: float, fila_b: int):
  # Ciclamos por la fila A para cambiar los valores
  for i in range(1, mat.columnas + 1):
    # NUEVO VALor
    nuevo_valor: float = escalar_a * mat.at(fila_a, i) + escalar_b * mat.at(fila_b, i)
    mat.set(fila_a, i, nuevo_valor)

# La misma operacion pero en resta
def restar_fila(mat: Matriz, fila_a: int, fila_b: int):
  # Ciclamos de nuevo por las columnas
  for i in range(1, mat.columnas + 1):
    # En la fila A, ponemos el resultado de A - B
    nuevo_valor: float = mat.at(fila_a, i) - mat.at(fila_b, i)
    mat.set(fila_a, i, nuevo_valor)

# Restar filas escaladas
# fa -> a*fa + b*fb
def restar_escalar_fila(mat: Matriz, escalar_a: float, fila_a: int, escalar_b: float, fila_b: int):
  # Ciclamos por la fila A para cambiar los valores
  for i in range(1, mat.columnas + 1):
    # NUEVO VALor
    nuevo_valor: float = escalar_a * mat.at(fila_a, i) - escalar_b * mat.at(fila_b, i)
    mat.set(fila_a, i, nuevo_valor)

# Intercambio de filas
# fa <-> fb
def intercambiar_fila(mat: Matriz, fila_a: int, fila_b: int):
  # Ciclamos de nuevo por las columnas
  for i in range(1, mat.columnas + 1):
    # Intercambiamos los valores
    temp: float = mat.at(fila_a, i)
    mat.set(fila_a, i, mat.at(fila_b, i))
    mat.set(fila_b, i, temp)

# Detectar si una fila es nula
def fila_nula(mat: Matriz, fila: int) -> bool:
  # Ciclamos de nuevo por las columnas
  for i in range(1, mat.columnas + 1):
    # Intercambiamos los valores
    if mat.at(fila, i) != 0:
      return False
  return True

# Operaciones basicas en una columna (por ahora solo una)
# Detectar si una columna es nula (0)
def columna_nula(mat: Matriz, columna: int) -> bool:
  # Ciclamos por todas las filas
  for i in range(1, mat.filas + 1):
    # Si encontramos un valor que no es 0, retornamos False
    if mat.at(i, columna) != 0:
      return False
  # Si no encontramos ningun valor que no es 0, retornamos True
  return True