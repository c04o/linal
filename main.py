import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt

class MatrixSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Crear secciones para entrada
        self.setup_dimension_inputs()
        
        # Inicializar tabla matriz
        self.matrix_table = None
        
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
        
        # Botón para generar la matriz
        self.generate_button = QPushButton("Generar matriz")
        self.generate_button.clicked.connect(self.generate_matrix_table)
        input_layout.addWidget(self.generate_button)
        
        # Añadir un espacio elástico para empujar todo a la izquierda
        input_layout.addStretch()
        
        self.main_layout.addLayout(input_layout)
    
    def generate_matrix_table(self):
        # Crear la cuadrícula de matriz editable basada en n y m
        n = self.n_spinbox.value() # Número de filas
        m = self.m_spinbox.value() # Número de columnas
        
        # Si una tabla ya existe, eliminarla primero
        if self.matrix_table:
            self.main_layout.removeWidget(self.matrix_table)
            self.matrix_table.deleteLater()

        # Crear el widget de tabla con n filas y m columnas
        self.matrix_table = QTableWidget(n, m)
        
        # Establecer encabezados (x1, x2, ..., i)
        headers = []
        for col in range(m):
            if col < m - 1:
                headers.append(f"x{col + 1}")
            else:
                headers.append("i") # La última columna es el vector del término independiente
        self.matrix_table.setHorizontalHeaderLabels(headers)
        
        # Expandir la tabla para llenar el espacio disponible
        self.matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Añadir la tabla a la estructura principal
        self.main_layout.addWidget(self.matrix_table)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixSolverApp()
    window.show()
    sys.exit(app.exec())
