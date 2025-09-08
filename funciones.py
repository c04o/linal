from matriz import Matriz
from posicion import Posicion
from operaciones import *
from auxiliar import pretty_number, to_subscript, termino_a_string

# Funcion para el output de los pasos
__pasos__ = 0


def imprimir_paso(texto_paso: str, mat: Matriz | None = None):
    # Esta instructiva es para decirle a python
    # que la variable pasos no es de la funcion, si no
    # una global
    global __pasos__
    __pasos__ += 1
    matriz_string: str = ""
    if mat is not None:
        matriz_string += mat.__str__()
    print(f"Paso #{__pasos__}: {texto_paso} \n{matriz_string}\n")

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

    print("Reduciendo matriz a forma escalonada reducida...")
    # Mientras estemos en los limites de la matriz
    while fila_pivote < filas and columna_pivote < columnas:
        # Nos movemos en la diagonal
        fila_pivote += 1
        columna_pivote += 1

        pivote: float = 0
        # Busquemos nuestro pivote
        while pivote == 0:
            # Obtenemos el numero en la posicion pivote
            pivote: float = mat.at(fila_pivote, columna_pivote)
            # Si no esta vacia la posicion del pivote, todo bien, ese es nuestro pivote
            if pivote != 0:
                break
            # Si no, tenemos que buscar otro en la misma columna
            encontrado: bool = False
            for i in range(fila_pivote + 1, filas + 1):
                # Si encontramos un buen candidato
                if mat.at(i, columna_pivote) != 0:
                    encontrado = True
                    # Intercambiamos las filas
                    intercambiar_fila(mat, i, fila_pivote)
                    # Ahora el nuevo numero esta en la posicion pivote
                    pivote: float = mat.at(fila_pivote, columna_pivote)
                    # Imprimimos el paso
                    imprimir_paso(
                        f"Intercambio de filas, f{fila_pivote} <-> f{i}", mat)

            # Si no encontramos el pivote, revisemos la siguiente columna
            if not encontrado:
                columna_pivote += 1
                # Si ya nos pasamos de las columnas de la matriz
                # sin encontrar un nuevo pivote, nuestro trabajo esta hecho
                if columna_pivote > columnas:
                    return

        # Ahora normalizamos la fila
        if pivote != 1:
            escalar_fila(mat, fila_pivote, 1 / pivote)
            # Imprimimos el paso
            imprimir_paso(
                f"Normalizar fila {fila_pivote}, f{fila_pivote} -> {pretty_number(1 / pivote)} * f{fila_pivote}", mat)

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
            imprimir_paso(
                f"Resta compuesta: f{i} -> f{i} - ({pretty_number(factor)}) * f{fila_pivote}", mat)

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
        # Tuve un problema de redondeo asi que si 10 digitos son 9 entonces podemos asegurarnos que es 1
        # o sea 0.999999999
        if round(pivote, 10) != 1:
            raise Exception(
                f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posicion de pivote")
        else:
            pivotes.append(Posicion(fila_actual, c))
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

    print("Reduciendo matriz a identidad...")
    for c in range(1, columnas + 1):
        # Obtenemos el pivote
        pivote: float = mat.at(fila_actual, c)
        # Si es 0, saltamos la columna actual
        if pivote == 0:
            continue
        # Si el pivote no es 1, nos mintieron, tiremos un error
        if round(pivote, 10) != 1:
            raise Exception(
                f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posicion de pivote")
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
            imprimir_paso(
                f"Resta compuesta: f{f} -> f{f} - ({pretty_number(factor)}) * f{fila_actual}", mat)
        # Finalmente, seguimos en la escalera para la fila de abajo
        fila_actual += 1
        # Si nos pasamos de las filas de la matriz, terminamos
        if fila_actual > filas:
            return

# Funcion para resolver un sistema de ecuaciones


def resolver_sistema(mat: Matriz, ecuaciones: int, incognitas: int):
    # Primero revisamos que las medidas de la matriz coincidan con los numeros dados
    if mat.filas != ecuaciones:
        raise Exception(
            "La cantidad de filas no coincide con la cantidad de ecuaciones")
    if mat.columnas != incognitas + 1:
        raise Exception(
            f"La cantidad de columnas esperada era: {incognitas + 1}, pero la dada fue: {mat.columnas}")
    columna_resultados: int = incognitas + 1

    # Ahora, colapsamos la matriz a su version escalonada reducida
    matriz_escalonada_reducida(mat, ecuaciones, incognitas)

    print(f"Matriz en forma Escalonada Reducida:\n{mat}\n")

    # Ahora revisaremos si es consistente
    # Revisemos todas las ecuaciones para asegurarnos que no existe una
    # contradiccion
    # Agregamos un 1 por la exclusividad del rango,
    # Si hago un range(1, 5) el resultado es [1..4]
    # necesito agregarle 1 para que quede [1..5]
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
            print("El sistema no tiene solución")
            print("Clasificación: Inconsistente.")
            # Terminamos nuestro trabajo
            return

    # Si no, revisamos las variables libres y las variables basicas
    # Basicamente, si una variable es basica, anotamos su numero de fila
    # si una variable es libre, la apuntamos como None
    # Iniciamos todas en None, cuando los pivotes nos digan lo contrario,
    # marcamos la correspondiente con su fila

    # x1 es libre
    # x2 es basica
    variables: list[int | None] = [None] * incognitas
    # Obtenemos los pivotes para saber cuantas variables libres tenemos
    pivotes: list[Posicion] = obtener_pivotes(mat, ecuaciones, incognitas)

    print(f"El sistema contiene {len(pivotes)} pivotes.")
    # Convertimos a matriz identidad para obtener los resultados
    matriz_identidad(mat, ecuaciones, incognitas)

    print(f"Matriz en forma identidad:\n{mat}\n")

    columnas_pivote: list[int] = []
    for i in range(0, len(pivotes)):
        print(f"Pivote #{i + 1}: {pivotes[i]}")
        # Si la columna del pivote actual no esta en columnas_pivote, la agregamos
        if pivotes[i].columna not in columnas_pivote:
            columnas_pivote.append(pivotes[i].columna)

    print(f"Columnas pivote: {columnas_pivote}")

    # Si el numero de pivotes es igual a las incognitas, el sistema tiene una unica solucion
    # y no hay variables libres
    if len(pivotes) == incognitas:
        print("\nLa matriz tiene una unica solución:\n")
        # Obtenemos los resultados de la columna de resultados
        for i in range(1, incognitas + 1):
            print(to_subscript(f"X{i} = ") +
                  f"{pretty_number(mat.at(i, columna_resultados))}")
    # De otra manera, imprimiremos el sistema con sus infinitas soluciones
    else:
        print("\nLa matriz tiene infinitas soluciones:\n")
        # Ciclamos por los pivotes para asignar las variables libres y basicas
        for pivote in pivotes:
            variables[pivote.columna - 1] = pivote.fila
        # Ahora imprimimos las variables basicas con sus condiciones, e imprimimos las variables libres
        for i in range(0, len(variables)):
            fila_variable = variables[i]

            # Si la variable es libre, es libre
            if fila_variable is None:
                print(to_subscript(f"X{i + 1} es libre"))
            else:
                # De otra manera, vamos a imprimir la ecuacion para la variable
                ecuacion: str = to_subscript(f"X{i + 1} = ")
                # Agregamos el numero primero
                resultado = mat.at(fila_variable, columna_resultados)
                # Esta variable nos indica cuando ya no es el primer termino, y no necesitamos ubicar el primer +
                primer_termino: bool = True
                # Si no es 0, lo agregamos a la ecuacion
                if resultado != 0:
                    ecuacion += termino_a_string(coeficiente=resultado,
                                                 variable=None, es_primer_termino=primer_termino)
                    primer_termino = False
                # Despues, agregamos el resto de variables como negativo (ya que quedarian con el signo volteado)
                # tras el despeje
                for columna in range(1, incognitas + 1):
                    # Si la columna es la variable, saltarsela
                    if columna == i + 1:
                        continue
                    # Si hay un coeficiente, entonces escribimos
                    coeficiente = mat.at(fila_variable, columna) * -1
                    ecuacion += termino_a_string(
                        coeficiente=coeficiente, variable=columna, es_primer_termino=primer_termino)
                    # Ya usamos el primer termino
                    if primer_termino == True:
                        primer_termino = False
                # Finalmente, imprimimos la variable con su ecuacion
                print(ecuacion)
    print("\nClasificacion: Consistente.")
