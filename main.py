import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QMessageBox, QSplitter)
from PySide6.QtCore import Qt
from classes import Matriz
from functions.gauss_jordan import resolver_gauss_jordan, establecer_funcion_print

class MatrixSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resolvedor de Matrices - Método de Gauss-Jordan")
        self.setMinimumSize(800, 600)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Crear secciones para entrada y resultados
        self.setup_input_section()
        self.setup_result_section()
        
    def setup_input_section(self):
        # Widget para la sección de entrada
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Crear secciones para entrada de dimensiones
        self.setup_dimension_inputs(input_layout)
        
        # Inicializar tabla matriz
        self.matrix_table = QTableWidget(3, 3)
        self.setup_matrix_table(input_layout)
        
        # Botón para resolver
        self.solve_button = QPushButton("Resolver Matriz")
        self.solve_button.clicked.connect(self.solve_matrix)
        input_layout.addWidget(self.solve_button)
        
        # Añadir a la sección principal
        self.main_layout.addWidget(input_widget, 1)
    
    def setup_result_section(self):
        # Widget para la sección de resultados
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        
        result_layout.addWidget(QLabel("Proceso y Resultados:"))
        
        # Área de texto para mostrar el proceso y resultados
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        
        # Añadir a la sección principal
        self.main_layout.addWidget(result_widget, 1)
    
    def setup_dimension_inputs(self, layout):
        # Interfaz para la entrada de las dimensiones de la matriz
        input_layout = QHBoxLayout()
        
        # Etiqueta y selector para filas (n)
        input_layout.addWidget(QLabel("Filas (n):"))
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setMaximum(10)
        self.n_spinbox.setValue(3)
        input_layout.addWidget(self.n_spinbox)
        
        # Etiqueta y selector para columnas (m)
        input_layout.addWidget(QLabel("Columnas (m):"))
        self.m_spinbox = QSpinBox()
        self.m_spinbox.setMinimum(2)
        self.m_spinbox.setMaximum(11)
        self.m_spinbox.setValue(3)
        input_layout.addWidget(self.m_spinbox)
        
        # Añadir un espacio elástico para empujar todo a la izquierda
        input_layout.addStretch()
        
        layout.addLayout(input_layout)
        
        # Conectar signals para actualización automática
        self.n_spinbox.valueChanged.connect(self.update_matrix_dimensions)
        self.m_spinbox.valueChanged.connect(self.update_matrix_dimensions)
    
    def setup_matrix_table(self, layout):
        # Configurar la tabla de matriz
        n = self.n_spinbox.value()
        m = self.m_spinbox.value()
        
        # Establecer encabezados (x1, x2, ..., i)
        headers = []
        for col in range(m):
            if col < m - 1:
                headers.append(f"x{col + 1}")
            else:
                headers.append("i")  # Última columna es el término independiente
        self.matrix_table.setHorizontalHeaderLabels(headers)
        
        # Expandir la tabla para llenar el espacio disponible
        self.matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Inicializar celdas con valor 0 si están vacías
        for row in range(n):
            for col in range(m):
                if self.matrix_table.item(row, col) is None:
                    self.matrix_table.setItem(row, col, QTableWidgetItem("0"))
        
        # Añadir la tabla a la estructura principal
        layout.addWidget(self.matrix_table)
    
    def update_matrix_dimensions(self):
        # Guardar datos existentes
        current_data = []
        current_rows = self.matrix_table.rowCount()
        current_cols = self.matrix_table.columnCount()
        
        for row in range(current_rows):
            row_data = []
            for col in range(current_cols):
                item = self.matrix_table.item(row, col)
                row_data.append(item.text() if item else "0")
            current_data.append(row_data)
        
        # Obtener nuevas dimensiones
        new_rows = self.n_spinbox.value()
        new_cols = self.m_spinbox.value()
        
        # Actualizar dimensiones de la tabla
        self.matrix_table.setRowCount(new_rows)
        self.matrix_table.setColumnCount(new_cols)
        
        # Actualizar encabezados
        headers = []
        for col in range(new_cols):
            if col < new_cols - 1:
                headers.append(f"x{col + 1}")
            else:
                headers.append("i")
        self.matrix_table.setHorizontalHeaderLabels(headers)
        
        # Restaurar datos existentes y llenar nuevas celdas
        for row in range(new_rows):
            for col in range(new_cols):
                if row < len(current_data) and col < len(current_data[0]):
                    # Celda existente - mantener valor
                    self.matrix_table.setItem(row, col, QTableWidgetItem(current_data[row][col]))
                else:
                    # Nueva celda - inicializar con 0
                    self.matrix_table.setItem(row, col, QTableWidgetItem("0"))
    
    def solve_matrix(self):
        # Obtener dimensiones
        n = self.n_spinbox.value()
        m = self.m_spinbox.value()
        
        if n + 1 != m:
          QMessageBox.warning(self, "Error", f"La matriz debe tener una dimension de n x n + 1")
          return
        
        # Creamos la matriz
        matriz: Matriz = Matriz(n, m)
        
        try:
            for row in range(0, n):
                for col in range(0, m):
                    item = self.matrix_table.item(row, col)
                    value = float(item.text()) if item and item.text() != "" else 0.0
                    # La matriz empieza a contar en 1 asi que tenemos que sumar 1 aca
                    matriz.set(row + 1, col + 1, value)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese solo valores numéricos en la matriz.")
            return
        
        # Aplicar el método de Gauss-Jordan
        # try:
        self.result_text.clear()
        funcion_print = self.result_text.append
        establecer_funcion_print(funcion_print)
        resolver_gauss_jordan(matriz)
        # except Exception as e:
        #     QMessageBox.warning(self, "Error", f"Error al resolver la matriz: {str(e)}")
        #     return
        
        # Mostrar los pasos y resultados
        # self.display_results(steps, result)
    
    def gauss_jordan(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        steps = []
        
        # Hacer una copia de la matriz para no modificar la original
        mat = [row[:] for row in matrix]
        
        steps.append(("Matriz original", self.format_matrix(mat)))
        
        # Aplicar eliminación de Gauss-Jordan
        for col in range(min(n, m-1)):
            # Encontrar el pivote (el elemento con mayor valor absoluto en la columna)
            pivot_row = col
            for row in range(col+1, n):
                if abs(mat[row][col]) > abs(mat[pivot_row][col]):
                    pivot_row = row
            
            # Intercambiar filas si es necesario
            if pivot_row != col:
                mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
                steps.append((f"Intercambiar fila {col+1} con fila {pivot_row+1}", self.format_matrix(mat)))
            
            # Si el pivote es cero, la matriz es singular
            if abs(mat[col][col]) < 1e-10:
                steps.append(("Pivote cero encontrado. La matriz puede ser singular.", ""))
                continue
            
            # Hacer el pivote igual a 1
            pivot_val = mat[col][col]
            for j in range(col, m):
                mat[col][j] /= pivot_val
            steps.append((f"Hacer pivote (fila {col+1}) igual a 1", self.format_matrix(mat)))
            
            # Hacer ceros en la columna actual
            for i in range(n):
                if i != col:
                    factor = mat[i][col]
                    for j in range(col, m):
                        mat[i][j] -= factor * mat[col][j]
                    steps.append((f"Eliminar elemento en fila {i+1}, columna {col+1}", self.format_matrix(mat)))
        
        # Determinar el resultado
        result = []
        for i in range(n):
            # Verificar si la fila es consistente
            all_zeros = all(abs(mat[i][j]) < 1e-10 for j in range(m-1))
            if all_zeros and abs(mat[i][m-1]) > 1e-10:
                result.append("Sistema inconsistente: 0 = " + str(mat[i][m-1]))
            elif all_zeros:
                result.append("Fila de ceros: infinitas soluciones")
            else:
                # Encontrar el pivote
                pivot_col = 0
                while pivot_col < m-1 and abs(mat[i][pivot_col]) < 1e-10:
                    pivot_col += 1
                if pivot_col < m-1:
                    result.append(f"x{pivot_col+1} = {mat[i][m-1]:.4f}")
        
        return steps, result
    
    def format_matrix(self, matrix):
        formatted = ""
        for row in matrix:
            formatted += "[" + " ".join(f"{val:8.3f}" for val in row) + "]\n"
        return formatted
    
    def display_results(self, steps, result):
        self.result_text.clear()
        self.result_text.append("=== PROCESO DE RESOLUCIÓN ===\n")
        
        for i, (description, matrix_str) in enumerate(steps):
            self.result_text.append(f"Paso {i+1}: {description}")
            if matrix_str:
                self.result_text.append(matrix_str)
        
        self.result_text.append("\n=== RESULTADOS ===")
        if result:
            for res in result:
                self.result_text.append(res)
        else:
            self.result_text.append("No se pudo determinar una solución única.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixSolverApp()
    window.show()
    sys.exit(app.exec())
