from matriz import Matriz
from posicion import Posicion
from operaciones import *

__funcion_imprimir__ = print

# Esta funcion existe para redirigir facilmente el output
# por ejemplo, a la hora de hacer el GUI, en lugar de usar print
# se va a tener que añadir los resultados a una caja de texto
def establecer_funcion_imprimir(func):
  global __funcion_imprimir__
  __funcion_imprimir__ = func

def imprimir(string: str):
  __funcion_imprimir__(string)

# Funcion para el output de los pasos
__pasos__ = 0
def imprimir_paso(string: str, mat: Matriz | None = None):
  # Esta instructiva es para decirle a python
  # que la variable pasos no es de la funcion, si no
  # una global
  global __pasos__
  __pasos__ += 1
  matriz_string: str = "\n"
  if mat is not None:
    matriz_string += mat.__str__()
  imprimir(f"Paso #{__pasos__}: {string} {matriz_string}") 

# Esta funcion convierte cualquier matriz a su forma escalonada reducida, esta se puede usar
# como fase primera en el algoritmo gauss_jordan

# La cantidad de filas y columnas son la submatriz que se desea reducir a forma escalonada
# (por ejemplo, en un sistema de ecuaciones, queremos reducir toda la matriz excepto la ultima columna)
def matriz_escalonada_reducida(mat: Matriz, filas: int, columnas: int):
  # Vamos a ciclar por todas las columnas de la matriz
  # Recordemos que range no incluye el ultimo numero, entonces necesitamos hacer un +1
  # para que el rango sea de 1 al numero de columnas
  fila_pivote = 0
  columna_pivote = 0
  
  imprimir("Reduciendo matriz a forma escalonada reducida...")
  # Mientras estemos en los limites de la matriz
  while fila_pivote < filas and columna_pivote < columnas:  
    # Nos movemos en la diagonal
    fila_pivote += 1
    columna_pivote += 1

    # Obtenemos el pivote
    pivote: float = mat.at(fila_pivote, columna_pivote)

    # Si es 0, buscamos alguna otra fila que podamos cambiar
    while pivote == 0:
      encontrado: bool = False
      # Si ya nos pasamos de las columnas de la matriz
      # sin encontrar un nuevo pivote, nuestro trabajo esta hecho
      if columna_pivote > columnas:
        return

      for i in range(fila_pivote + 1, filas + 1):
        # Si encontramos un buen candidato
        if mat.at(i, columna_pivote) != 0:
          encontrado = True
          # Intercambiamos las filas
          intercambiar_fila(mat, i, fila_pivote)
          # Ahora el nuevo numero esta en la posicion pivote
          pivote: float = mat.at(fila_pivote, columna_pivote)
          # Imprimimos el paso
          imprimir_paso(f"Intercambio de filas, f{fila_pivote} <-> f{i}", mat)
      
      # Si no encontramos el pivote, revisemos la siguiente columna
      if not encontrado:
        columna_pivote += 1
    
    # Ahora normalizamos la fila
    if pivote != 1:
      escalar_fila(mat, fila_pivote, 1 / pivote)
      # Imprimimos el paso
      imprimir_paso(f"Normalizar fila {fila_pivote}, f{fila_pivote} -> ({1/pivote:.2f}) * f{fila_pivote}", mat)
    
    # Y dejamos en 0 todas las filas abajo del pivote
    for i in range(fila_pivote + 1, filas + 1):
      # El factor es el numero que encontremos
      factor: float = mat.at(i, columna_pivote)
      # Si el factor ya es 0, no necesitamos hacer nada
      if factor == 0:
        continue
      # Ahora multiplicamos la fila pivote por el factor y la restamos a la actual
      # de esta manera, si nos encontramos 2, restamos 2 veces la fila principal, cuyo pivote es siempre 1
      # gracias a la normalizacion hecha previamente
      restar_escalar_fila(mat, 1, i, factor, fila_pivote)
      # Imprimimos el paso
      imprimir_paso(f"Resta compuesta de filas, f{i} -> f{i} - ({factor:.2f}) * f{fila_pivote}", mat)

# Esta funcion obtiene los pivotes de una matriz escalonada reducida
def obtener_pivotes(mat: Matriz, filas: int, columnas: int):
  # Pivotes, son una tupla de 2 enteros
  # porque contienen informacion de su fila y columna
  pivotes: list[Posicion] = []
  # Ciclamos por todas las columnas
  fila_actual = 1

  for c in range(1, columnas + 1):
    # Obtenemos el pivote
    pivote: float = mat.at(fila_actual, c)
    # Si es 0, saltamos la columna actual
    if pivote == 0:
      continue
    # Si el pivote no es 1, nos mintieron, tiremos un error
    if pivote != 1:
      raise Exception(f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posicion de pivote")
    else: pivotes.append(Posicion(fila_actual, c))
    # Finalmente, seguimos en la escalera para la fila de abajo
    fila_actual += 1
    # Si nos pasamos de las filas de la matriz, terminamos
    if fila_actual > filas:
      return pivotes
    
  return pivotes
  
# Esta funcion transforma una matriz escalonada reducida a una matriz identidad
# Para que esta funcion, funcione, la matriz DEBE ser escalonada reducida,
# se puede reducir con la funcion matriz_escalonada_reducida

# La funcion sigue sirviendo si la matriz tiene multiples soluciones,
# esta funcion colapsara todas las variables basicas en todas las filas,
# dejando tan solo las variables libres
def matriz_identidad(mat: Matriz, filas: int, columnas: int):
  # Ciclamos por todas las columnas para ir reduciendo cada una
  fila_actual = 1
  
  for c in range(1, columnas + 1):
    # Obtenemos el pivote
    pivote: float = mat.at(fila_actual, c)
    # Si es 0, saltamos la columna actual
    if pivote == 0:
      continue
    # Si el pivote no es 1, nos mintieron, tiremos un error
    if pivote != 1:
      raise Exception(f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posicion de pivote")
    # Si no, actualizamos la fila
    # Ciclamos por todos los espacios arriba del pivote para reducirlas
    for f in range(1, fila_actual):
      # El factor es el numero que encontremos
      factor: float = mat.at(f, c)
      # Si el factor ya es 0, no necesitamos hacer nada
      if factor == 0:
        continue
      # Ahora multiplicamos la fila pivote por el factor y la restamos a la actual
      # de esta manera, si nos encontramos 2, restamos 2 veces la fila principal, cuyo pivote es siempre 1
      # gracias a la normalizacion hecha previamente
      restar_escalar_fila(mat, 1, f, factor, fila_actual)
      # Imprimimos el paso
      imprimir_paso(f"Resta compuesta de filas, f{f} -> f{f} - ({factor:.2f}) * f{fila_actual}", mat)
    # Finalmente, seguimos en la escalera para la fila de abajo
    fila_actual += 1
    # Si nos pasamos de las filas de la matriz, terminamos
    if fila_actual > filas:
      return

# Funcion para resolver un sistema de ecuaciones
def resolver_sistema(mat: Matriz, ecuaciones: int, incognitas: int):
  # Primero revisamos que las medidas de la matriz coincidan con los numeros dados
  if mat.filas != ecuaciones:
    raise Exception("La cantidad de filas no coincide con la cantidad de ecuaciones")
  if mat.columnas != incognitas + 1:
    raise Exception(f"La cantidad de columnas esperada era: {incognitas + 1}, pero la dada fue: {mat.columnas}")
  columna_resultados: int = incognitas + 1
  
  # Ahora, colapsamos la matriz a su version escalonada reducida
  matriz_escalonada_reducida(mat, ecuaciones, incognitas)

  imprimir(f"Matriz en forma Escalonada Reducida:\n{mat}\n")
  
  # Ahora revisaremos si es consistente
  # Revisemos todas las ecuaciones para asegurarnos que no existe una
  # contradiccion
  for fila in range(1, ecuaciones + 1):
    # Revisar si la fila son solo ceros 
    fila_nula: bool = True
    # Ciclamos hasta encontrar un elemento distinto de cero
    for columna in range(1, incognitas + 1):
      if mat.at(fila, columna) != 0:
        fila_nula = False
        break
    # Si la fila es nula, pero el resultado no, quiere decir que nos estamos contradiciendo,
    # por ende, el sistema es inconsistente
    if fila_nula and mat.at(fila, columna_resultados) != 0:
      imprimir("El sistema es inconsistente")
  
  # Si no, revisamos las variables libres y las variables basicas
  # Basicamente, si una variable es basica, anotamos su numero de fila
  # si una variable es libre, la apuntamos como None
  # Iniciamos todas en None, cuando los pivotes nos digan lo contrario,
  # marcamos la correspondiente con su fila
  variables: list[int | None] = [None] * incognitas
  # Obtenemos los pivotes para saber cuantas variables libres tenemos
  pivotes: list[Posicion] = obtener_pivotes(mat, ecuaciones, incognitas)

  imprimir(f"El sistema contiene {len(pivotes)} pivotes.")
  # Convertimos a matriz identidad para obtener los resultados
  matriz_identidad(mat, ecuaciones, incognitas)

  for i in range(0, len(pivotes)):
    imprimir(f"Pivote #{i}: {pivotes[i]}")
  # Si el numero de pivotes es igual a las incognitas, el sistema tiene una unica solucion
  # y no hay variables libres
  if len(pivotes) == incognitas:
    imprimir("\nLa matriz tiene una unica solución:\n")
    # Obtenemos los resultados de la columna de resultados
    for i in range(1, incognitas + 1):
      imprimir(f"X{i} = {mat.at(i, columna_resultados)}")
  # De otra manera, imprimiremos el sistema con sus infinitas soluciones
  else:
    imprimir("\nLa matriz tiene infinitas soluciones:\n")
    # Ciclamos por los pivotes para asignar las variables libres y basicas
    for pivote in pivotes:
      variables[pivote.columna - 1] = pivote.fila
    # Ahora imprimimos las variables basicas con sus condiciones, e imprimimos las variables libres
    for i in range(0, len(variables)):
      fila_variable = variables[i]

      if fila_variable == None:
        imprimir(f"X{i + 1} es libre")
      else:
        # De otra manera, vamos a imprimir la ecuacion para la variable
        ecuacion: str = ""
        # Agregamos el numero primero
        resultado = mat.at(fila_variable, columna_resultados)
        # Si no es 0, lo agregamos a la ecuacion
        if resultado != 0:
          ecuacion += f"{resultado}"
        # Despues, agregamos el resto de variables como negativo (ya que quedarian con el signo volteado)
        # tras el despeje
        for columna in range(1, incognitas + 1):
          # Si la columna es la variable, saltarsela
          if columna == i + 1:
            continue
          # Si hay un coeficiente, entonces escribimos
          coeficiente = mat.at(fila_variable, columna) * -1
          if coeficiente != 0:
            # Obtenemos el coeficiente puro, el signo lo añadiremos nosotros
            coeficiente_sin_signo = abs(coeficiente)
            # Añadimos el signo
            if coeficiente >= 0:
              ecuacion += " + "
            else:
              ecuacion += " - "
            # Ahora añadimos la variable
            ecuacion += f"({coeficiente_sin_signo})X{columna}"
        # Finalmente, imprimimos la variable con su ecuacion
        imprimir(f"X{i + 1} = {ecuacion}")
