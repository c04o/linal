from matriz import Matriz
from operaciones import *

# Esta funcion retorna:
# -1 si hubo un error a la hora de operar (matriz invalida)
# 0 si no existen soluciones (contradiccion)
# 1 si existen infinitas soluciones
# Arreglo de numeros (floats) si existe una sola solucion
def gauss_jordan(mat: Matriz, debug:bool = False) -> int | list[float]:
  # Para un sistema de ecuaciones, la matriz debe ser de n x n+1
  if(mat.columnas != mat.filas + 1):
    print(f"La matriz debe ser de n x n+1, y las dimensiones dadas fueron de {mat.filas}x{mat.columnas}")
    return -1
  
  # Numero de filas, o el tamaño real de la matriz
  n: int = mat.filas

  # Empezamos el proceso
  for col in range(1, n+1):
    if debug: print(f"Paso #{col}: \n{mat}")
    # Si la columna esta vacia, la ignoramos
    if columna_nula(mat, col):
      continue

    # Buscamos el pivote
    pivote: float = mat.at(col, col)

    # Si el pivote es 0, busquemos un numero en la columna actual para buscar un pivote
    if pivote == 0:
      # Busquemos una fila abajo con un pivote distinto de 0
      for k in range(col + 1, n + 1):
        # Si encontramos un potencial pivote, intercambiamos las filas para dejarlo
        # en la posicion primordial
        if mat.at(k, col) != 0:
          intercambiar_fila(mat, col, k)
          pivote = mat.at(col, col)
          break
    
    # Si el pivote es 0, ya no queda nada mas que hacer
    if pivote == 0:
      continue
    # Normalizar la fila del pivote
    if pivote != 1:
      escalar_fila(mat, col, 1 / pivote)
    
    # Hacer ceros en la columna del pivote para las otras filas
    for fila in range(1, n+1):
      # No queremos afectar la fila que contiene el pivote actual
      if fila != col:
        factor: float = mat.at(fila, col)
        # Como la fila pivote ya esta normalizada, simplemente la restamos
        # fj -> fj - factor * fi
        restar_escalar_fila(mat, 1, fila, factor, col)

    if debug: print(f"Despues de paso #{col}: \n{mat}")

  # Esto nos dejara una matriz triangular superior, aqui quedaria matriz identidad,
  # en cualquier otro caso, no tiene solucion o tiene infinitas
  if debug: print(f"Matriz despues de despeje:\n{mat}")

  for i in range(1, n+1):
    # Verificar filas inconsistentes (0 = b donde b ≠ 0)
    fila_es_cero = True
    for j in range(1, n+1):
      if mat.at(i, j) != 0:
        fila_es_cero = False
        break
            
    if fila_es_cero and mat.at(i, n+1) != 0:
      return 0  # Sistema inconsistente
  
  # Contar variables básicas
  variables_basicas = 0
  for i in range(1, n+1):
    if not fila_nula(mat, i):
      variables_basicas += 1
  
  if variables_basicas < n:
    return 1  # Infinitas soluciones
  
  soluciones: list[float] = [0] * n

  # Extraer soluciones directamente de la matriz identidad
  for i in range(1, n+1):
    # Buscar el pivote en esta fila (debería estar en la diagonal)
    if mat.at(i, i) == 1:
      soluciones[i-1] = mat.at(i, n+1)
    else:
      print(f"Hubo un problema generando el conjunto solucion")
      return -1
  
  return soluciones

def resolver_gauss_jordan(mat: Matriz, debug:bool = False):
  valor_retorno: int | list[float] = gauss_jordan(mat, debug)

  match valor_retorno:
    # Checamos los codigos de error
    case -1:
      print("Hubo un problema aplicando el metodo gauss-jordan")
    case 0:
      print("No existen soluciones")
    case 1:
      print("Existen infinitas soluciones")
    case _:
      # Asertamos que valor retorno es una lista entonces
      # (el asertar es para que el interpretador no llore
      assert valor_retorno is list[float]

      print("Soluciones:")
      for i in range(0, len(valor_retorno)):
        print(f"X{i + 1} = {valor_retorno[i]}")