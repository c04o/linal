from auxiliar import pretty_number


class Matriz:
    # Representa a la matriz,
    matriz: list[list[float]] = []
    filas = 0
    columnas = 0

    # Constructor de la clase
    def __init__(self, filas: int, columnas: int):
        if filas <= 0 or columnas <= 0:
            # Tiramos un error si alguno de los dos numeros es invalido
            raise Exception(
                "El numero de filas y columnas tienen que ser mayores a 0")

        # Rellenamos las filas y columnas
        self.filas = filas
        self.columnas = columnas
        self.matriz = []

        for i in range(0, filas):
            # Inicializamos cada una de las filas
            self.matriz.append([])
            for _ in range(0, columnas):
                # Inicializamos todo a 0
                self.matriz[i].append(0)

    # Check de limites
    # Lo puse entre dos barras bajas porque es un metodo 'privado' (no lo va a usar el usuario de la clase)
    def _boundcheck_(self, fila: int, columna: int):
        if fila > self.filas or columna > self.columnas or fila <= 0 or columna <= 0:
            raise Exception(
                f"Sobrepaso de indice, se pidió la posición ({fila},{columna}) en una matriz de {self.filas}x{self.columnas}")

    # Indice
    def at(self, fila: int, columna: int) -> float:
        self._boundcheck_(fila, columna)
        # como los arreglos en python empiezan a contar de 0, restemos 1
        # asi la posicion #1 se convierte a 0, la verdadera posicion inicial
        return self.matriz[fila-1][columna-1]

    # Set
    def set(self, fila: int, columna: int, valor: float):
        self._boundcheck_(fila, columna)
        # Explicacion en la funcion d arriba
        self.matriz[fila - 1][columna - 1] = valor

    # El metodo to string (para que pueda imprimirse)
    # este es un metodo por defecto de python, algo asi como el constructor
    def __str__(self) -> str:
        # El string
        string = ""

        # Imprimimos la matriz entera
        for i in range(0, self.filas):
            for j in range(0, self.columnas):
                # Agregamos la celda
                # Esto se ve complicado pero basicamente solo es imprimir el objeto actual
                # solo dos decimales en float, encerrado entre dos corchetes y una tabulacion al final
                string += "[" + f"{pretty_number(self.matriz[i][j])}" + "]\t"
            # Salto de linea
            string += '\n'

        return string
