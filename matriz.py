class Matriz:
  # Representa a la matriz,
  matriz: list[list[int]] = []
  filas: int = -1
  columnas: int = -1

  # Constructor de la clase
  def __init__(self, filas, columnas):
    if filas <= 0 or columnas <= 0:
      # Tiramos un error si alguno de los dos numeros es invalido
      raise "El numero de filas y columnas tienen que ser mayores a 0"

    # Rellenamos las filas y columnas
    self.filas = filas
    self.columnas = columnas
    self.matriz = []

    for i in range(0, filas):
      # Inicializamos cada una de las filas
      self.matriz.append([])
      for j in range(0, columnas):
        # Inicializamos todo a 0
        self.matriz[i].append(0)
  
  # Indice
  def at(self, fila, columna):
    if fila > self.filas or columna > self.columnas:
      raise f"Sobrepaso de indice, se pidió la posición ({fila},{columna}) en una matriz de {self.filas}x{self.columnas}"
    # como los arreglos en python empiezan a contar de 0, restemos 1
    # asi la posicion #1 se convierte a 0, la verdadera posicion inicial
    return self.matriz[fila-1][columna-1]
  
  # Set
  def set(self, fila, columna, valor):
    if fila > self.filas or columna > self.columnas:
      raise f"Sobrepaso de indice, se pidió la posición ({fila},{columna}) en una matriz de {self.filas}x{self.columnas}"
    # Explicacion en la funcion d arriba
    self.matriz[fila - 1][columna - 1] = valor

  # El metodo to string (para que pueda imprimirse)
  def __str__(self):
    # El string
    string = ""

    # Imprimimos la matriz entera
    for i in range(0, self.filas):
      for j in range(0, self.columnas):
        # Agregamos la celda
        string += f"[{self.matriz[i][j]}]"
      # Salto de linea
      string += '\n'
    
    return string