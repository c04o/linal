class Posicion:
    fila: int
    columna: int

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return f"({self.fila},{self.columna})"
