import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt

class MatrixSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resolvedor de Matrices - Método de Gauss")
        self.setMinimumSize(600, 400)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Crear secciones para entrada
        self.setup_dimension_inputs()
        
        # Inicializar tabla matriz
        self.matrix_table = QTableWidget(3, 3)  # Tamaño inicial
        self.setup_matrix_table()
        
        # Conectar signals para actualización automática
        self.n_spinbox.valueChanged.connect(self.update_matrix_dimensions)
        self.m_spinbox.valueChanged.connect(self.update_matrix_dimensions)
        
    def setup_dimension_inputs(self):
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
        
        self.main_layout.addLayout(input_layout)
    
    def setup_matrix_table(self):
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
        self.matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Inicializar celdas con valor 0 si están vacías
        for row in range(n):
            for col in range(m):
                if self.matrix_table.item(row, col) is None:
                    self.matrix_table.setItem(row, col, QTableWidgetItem("0"))
        
        # Añadir la tabla a la estructura principal
        self.main_layout.addWidget(self.matrix_table)
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixSolverApp()
    window.show()
    sys.exit(app.exec())
