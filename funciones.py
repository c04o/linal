from matriz import Matriz
from operaciones import *

def gauss_jordan(mat: Matriz):
  # Para un sistema de ecuaciones, la matriz debe ser de n x n+1
  if(mat.columnas != mat.filas + 1):
    print(f"La matriz debe ser de n x n+1, y las dimensiones dadas fueron de {mat.filas}x{mat.columnas}")
    return
  
  # Numero de filas, o el tamaño real de la matriz
  # Por ejemplo, si el sistema tiene 3 variables,
  # o sea, 3x3, el tamaño de la matriz va a ser 3 x 4
  # pero todos los datos que nos interesan estan en la submatriz
  # 3x3, entonces solo queremos visitar hasta n
  n: int = mat.filas
  # Este es el numero de pasos que llevamos
  pasos: int = 1

  # Empezamos el proceso
  # Voy a documentar todo lo que pueda aqui asi que pongan mucha atencion:
  # El algoritmo tiene 3 partes:
  
  # GENERACION DE PIVOTE
  # Basicamente, queremos que todos nuestros pivotes esten en la diagonal principal
  # para lograr esto, tenemos que verificar que la columna no este vacia (todos 0, en cuyo caso no se podra obtener una unica solucion)
  # y, en el caso que la posicion pivote sea 0, intercambiarla con alguna otra fila para que deje de serlo
  
  # NORMALIZACION DE LA FILA
  # Si el pivote es 2, escalamos la fila por 1/2
  # Si el pivote es -3, escalamos la fila por -1/3
  # de esta manera, obtendremos el valor pivote en 1 y el siguiente
  # paso sera mucho mas facil

  # REDUCCION DE LA COLUMNA
  # Ya que tenemos nuestro pivote en 1, queremos convertir el resto de la columna en 0s
  # esto nos va a ayudar a reducir la matriz hasta la forma identidad, en donde tendremos
  # nuestros resultados.
  # Para esto, necesitamos restar a las otras filas
  # por ejemplo, digamos que tenemos estas 2 filas:
  # [1][4][2]
  # [2][6][5]
  # Ya tenemos nuestro pivote en la primera columna
  # sin embargo, queremos que todos los elementos en la primera columna
  # menos el pivote sean 0, como logramos esto?
  # Bueno, que numero tengo que restarle a 2 para que sea 0, obviamente, 2
  # y que numero le tengo que multiplicar a 1 para que me de 2? obviamente, tambien 2
  # Pues, en este caso, necesitamos restarle a la segunda fila la primera fila multiplicada por dos
  # Tal que: f2 -> f2 - 2 * f1
  # De esta manera, con el resto de columnas que no sean el pivote (entiendan que el pivote es el elemento que esta en la diagonal)
  # Como el pivote ya se normalizo, y es 1, simplemente tenemos que restar la fila del pivote por el valor que queremos eliminar
  # entonces si el valor es [n], queremos hacer la operacion: f -> f - n * fp
  # Todo esto va a eventualmente generar 0s en todos los campos menos la diagonal, y nos va a dejar con una matriz identidad
  # Ahora, esto no es cierto siempre, porque el sistema puede ser inconsistente o tener infinitas soluciones, pero eso se
  # comprobara mas tarde

  # Ciclamos por todas las columnas para generar nuestros pivotes
  # Recuerden que como range es excluyente, tenemos que usar el + 1
  # entonces de esa manera vamos en el rango de 1 a n (la columna de los resultados se ignora)
  for i in range(1, n + 1):
    # Si la columna esta vacia, la ignoramos
    if columna_nula(mat, i):
      continue

    # === GENERACION DEL PIVOTE ===
    # Buscamos el pivote (posicion i x i, porque vamos en diagonal)
    pivote: float = mat.at(i, i)

    # Si el pivote es 0, busquemos un numero (diferente a 0) en la columna actual para volverlo el pivote
    if pivote == 0:
      # Busquemos una fila abajo con un pivote distinto de 0
      for k in range(i + 1, n + 1):
        # Si encontramos un potencial pivote, intercambiamos las filas para dejarlo
        # en la posicion pivotal (o sea, en la diagonal)
        if mat.at(k, i) != 0:
          # Intercambiamos la fila
          intercambiar_fila(mat, i, k)
          # Actualizamos el pivote (que ahora si esta en la posicion de la diagonal)
          pivote = mat.at(i, i)
          # Imprimimos
          print(f"Paso #{pasos}:")
          # Imprimimos el paso
          print(f"Intercambio de filas: f{i} <-> f{k}")
          # Imprimimos la matriz
          print(mat)
          # Aumentamos el numero de pasos
          pasos += 1
          break
    
    # Si el pivote sigue siendo 0, no podemos hacer nada mas
    if pivote == 0:
      continue

    # === NORMALIZACION DE LA FILA ===
    # Normalizar la fila del pivote
    if pivote != 1:
      # Escalamos la fila
      escalar_fila(mat, i, 1 / pivote)
      # Imprimimos
      print(f"Paso #{pasos}:")
      # Imprimimos el paso
      print(f"Escalacion de fila: f{i} -> ({1/pivote:.2f}) * f{i}")
      # Imprimimos la matriz
      print(mat)
      # Aumentamos el numero de pasos
      pasos += 1
    
    # === REDUCCION DE LA COLUMNA ===
    # Hacer ceros en la columna del pivote para las otras filas
    for fila in range(1, n+1):
      # No queremos afectar la fila que contiene el pivote actual
      # asi que vamos a reducir SOLO si la fila actual no es la fila que contiene al pivote
      if fila != i:
        # El factor es el numero que obtenemos,
        # si el numero es 2, tenemos que restar 2 veces la fila del pivote,
        # si el numero es -3, tenemos que restar -3 veces la fila del pivote
        factor: float = mat.at(fila, i)
        # Como la fila pivote ya esta normalizada, simplemente la restamos
        # fj -> fj - factor * fi
        restar_escalar_fila(mat, 1, fila, factor, i)
        # Hacemos la impresion del paso
        print(f"Paso #{pasos}:")
        # Imprimimos el paso
        print(f"Resta de filas: f{fila} -> f{fila} - ({factor:.2f}) * f{i}")
        # Imprimimos la matriz
        print(mat)
        # Aumentamos el numero de pasos
        pasos += 1

  # VERIFICAMOS SI EL SISTEMA ES INCONSISTENTE
  # el algoritmo anterior deberia dejarnos con una matriz identidad, hay dos casos donde esto no se cumple:
  # 1. El sistema tiene infinitas soluciones
  # en este caso, la matriz restante tendra una fila nula o vacia, o sea:
  # [0][0][0][0]
  # debido a esto, la variable de esta fila es libre y por ende el sistema no se puede resolver
  # 2. El sistema no tiene ninguna solucion (es inconsistente)
  # en este caso, la matriz restante tendra un resultado contradictorio, como:
  # [0][0][0][4]
  # Como una suma de valores multiplicados por 0 no puede dar otra cosa que no sea 0,
  # esto es una contradiccion, entonces, buscamos por una contradiccion asi para verificar si el
  # sistema es inconsistente
  for i in range(1, n+1):
    # Verificar si la fila excepto el resultado es todo 0s [0][0][0]
    fila_es_cero = True
    # Ciclamos por todos los elementos de la fila
    for j in range(1, n+1):
      # Si alguno no es 0
      if mat.at(i, j) != 0:
        # Establecemos que la fila no es 0 y rompemos el ciclo
        fila_es_cero = False
        break
            
    # Si la fila es 0, pero el resultado no, es una contradiccion, sistema inconsistente
    if fila_es_cero and mat.at(i, n+1) != 0:
      print("El sistema no tiene solución")
      # El return es para que salgamos ya de la funcion, porque ya tenemos nuestro resultado
      return

  # Ahora que sabemos que no hay contradicciones,
  # si existe alguna fila nula, hay una variable libre,
  # por ende, infinitas soluciones
  for i in range(1, n+1):
    if fila_nula(mat, i):
      print("El sistema tiene infinitas soluciones")
      # Se explica arriba porque hay un return
      return
  
  # Creamos una lista
  soluciones: list[float] = []

  # Extraer soluciones directamente de la matriz identidad
  # Estamos ciclando de 1 a n, pero como los rangos son exclusivos en python, necesitamos usar n + 1
  # El rango [1, n+1) es [1, 2, 3 ... n]
  for i in range(1, n+1):
    # Por cada fila, buscaremos la solucion (fila actual, columna n + 1)
    soluciones.append( mat.at(fila=i, columna=n+1) )
  
  # Ahora imprimimos todas las soluciones
  # Usamos un for para ciclar por el arreglo de soluciones
  for i in range(0, len(soluciones)):
    # Imprimimos el numero de variable y su resultado
    # Como los arreglos empiezan de 0, tenemos que sumarle 1
    # para que en lugar de imprimir empezando de 0, imprima empezando de 1
    # si no el resultado se veria algo asi:
    # x0 = 2.0
    # x1 = -3.5
    # x3 = 4.5
    # y nosotros no queremos eso verdad?
    print(f"X{i + 1} = {soluciones[i]:.2f}")