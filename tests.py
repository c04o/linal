import unittest
import io
from contextlib import redirect_stdout
from matriz import Matriz
from funciones import gauss_jordan
from operaciones import *

class TestMatriz(unittest.TestCase):
    def test_probar_limites(self):
        mat = Matriz(3, 4)
        with self.assertRaises(Exception): mat.at(3, 5)
        with self.assertRaises(Exception): mat.at(4, 3)
        with self.assertRaises(Exception): mat.at(0, 0)
        with self.assertRaises(Exception): mat.at(-1, 2)
        self.assertEqual(mat.at(2,2), 0)

class TestOperaciones(unittest.TestCase):
    def setUp(self):
        self.mat = Matriz(2, 2)
        self.mat.set(1, 1, 1)
        self.mat.set(1, 2, 2)
        self.mat.set(2, 1, 3)
        self.mat.set(2, 2, 4)

    def test_escalar_fila(self):
        escalar_fila(self.mat, 1, 2)
        self.assertEqual(self.mat.at(1, 1), 2)
        self.assertEqual(self.mat.at(1, 2), 4)

    def test_sumar_fila(self):
        sumar_fila(self.mat, 1, 2)
        self.assertEqual(self.mat.at(1, 1), 4)
        self.assertEqual(self.mat.at(1, 2), 6)

    def test_sumar_escalar_fila(self):
        sumar_escalar_fila(self.mat, 2, 1, 3, 2)
        self.assertEqual(self.mat.at(1, 1), 2*1 + 3*3)
        self.assertEqual(self.mat.at(1, 2), 2*2 + 3*4)

    def test_restar_fila(self):
        restar_fila(self.mat, 2, 1)
        self.assertEqual(self.mat.at(2, 1), 2)
        self.assertEqual(self.mat.at(2, 2), 2)

    def test_restar_escalar_fila(self):
        restar_escalar_fila(self.mat, 2, 2, 1, 1)
        self.assertEqual(self.mat.at(2, 1), 2*3 - 1*1)
        self.assertEqual(self.mat.at(2, 2), 2*4 - 1*2)

    def test_intercambiar_fila(self):
        intercambiar_fila(self.mat, 1, 2)
        self.assertEqual(self.mat.at(1, 1), 3)
        self.assertEqual(self.mat.at(2, 1), 1)

    def test_fila_nula(self):
        mat = Matriz(1, 3)
        self.assertTrue(fila_nula(mat, 1))
        mat.set(1, 2, 5)
        self.assertFalse(fila_nula(mat, 1))

    def test_columna_nula(self):
        mat = Matriz(3, 2)
        self.assertTrue(columna_nula(mat, 1))
        mat.set(2, 1, 7)
        self.assertFalse(columna_nula(mat, 1))

class TestGaussJordan(unittest.TestCase):
    def _capturar_output(self, mat):
        buf = io.StringIO()
        with redirect_stdout(buf):
            gauss_jordan(mat)
        return buf.getvalue()

    def test_solucion_unica(self):
        mat = Matriz(3, 4)
        datos = [
            [2, 1, -1, 8],
            [-3, -1, 2, -11],
            [-2, 1, 2, -3]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)

        # Verifica que se imprimieron las soluciones esperadas
        self.assertIn("X1 = 2.00", salida)
        self.assertIn("X2 = 3.00", salida)
        self.assertIn("X3 = -1.00", salida)

    def test_infinitas_soluciones(self):
        mat = Matriz(3, 4)
        datos = [
            [1, 2, -1, 3],
            [2, 4, -2, 6],
            [3, 6, -3, 9]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("El sistema tiene infinitas soluciones", salida)

    def test_sin_solucion(self):
        mat = Matriz(2, 3)
        datos = [
            [1, -1, 2],
            [2, -2, 5]
        ]
        for i in range(2):
            for j in range(3):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("El sistema no tiene solución", salida)

    def test_matriz_invalida(self):
        mat = Matriz(2, 2)
        salida = self._capturar_output(mat)
        self.assertIn("La matriz debe ser de n x n+1", salida)

    def test_sistema_identidad(self):
        """Prueba con matriz identidad (solución trivial)"""
        mat = Matriz(3, 4)
        datos = [
            [1, 0, 0, 5],
            [0, 1, 0, 3],
            [0, 0, 1, 7]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        
        self.assertIn("X1 = 5", salida)
        self.assertIn("X2 = 3", salida)
        self.assertIn("X3 = 7", salida)

    def test_sistema_triangular_superior(self):
        """Prueba con matriz triangular superior"""
        mat = Matriz(3, 4)
        datos = [
            [2, 1, 3, 13],
            [0, 4, 2, 14],
            [0, 0, 3, 9]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        
        self.assertIn("X1 = 1.00", salida)
        self.assertIn("X2 = 2.00", salida)
        self.assertIn("X3 = 3.00", salida)

    def test_sistema_triangular_inferior(self):
        """Prueba con matriz triangular inferior"""
        mat = Matriz(3, 4)
        datos = [
            [3, 0, 0, 6],
            [2, 4, 0, 14],
            [1, 1, 2, 8]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        
        self.assertIn("X1 = 2.00", salida)
        self.assertIn("X2 = 2.50", salida)
        self.assertIn("X3 = 1.75", salida)

    def test_sistema_con_pivote_cero(self):
        """Prueba donde se necesita intercambio de filas por pivote cero"""
        mat = Matriz(3, 4)
        datos = [
            [0, 2, 3, 13],
            [1, 1, 1, 6],
            [2, 3, 4, 17]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("X1 = -2.00", salida)
        self.assertIn("X2 = 11.00", salida)
        self.assertIn("X3 = -3.00", salida)

    def test_sistema_con_numeros_decimales(self):
        """Prueba con números decimales"""
        mat = Matriz(3, 4)
        datos = [
            [0.5, 1.2, -0.3, 3.4],
            [1.5, -0.4, 0.7, 4.6],
            [-0.7, 0.9, 1.1, 5.7]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("X1 = 2.00", salida)
        self.assertIn("X2 = 3.00", salida)
        self.assertIn("X3 = 4.00", salida)

    def test_sistema_2x2_simple(self):
        """Prueba con sistema 2x2 simple"""
        mat = Matriz(2, 3)
        datos = [
            [2, 3, 8],
            [1, 2, 5]
        ]
        for i in range(2):
            for j in range(3):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("X1 = 1.00", salida)
        self.assertIn("X2 = 2.00", salida)

    def test_sistema_con_coeficientes_negativos(self):
        """Prueba con coeficientes negativos"""
        mat = Matriz(2, 3)
        datos = [
            [-2, 3, 1],
            [4, -1, 7]
        ]
        for i in range(2):
            for j in range(3):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("X1 = 2.20", salida)
        self.assertIn("X2 = 1.80", salida)

    def test_sistema_4x4(self):
        """Prueba con sistema 4x4"""
        mat = Matriz(4, 5)
        datos = [
            [2, 1, -1, 1, 8],
            [-3, -1, 2, -1, -11],
            [-2, 1, 2, -1, -3],
            [1, -1, 1, 2, 9]
        ]
        for i in range(4):
            for j in range(5):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("X1 = 9.33", salida)
        self.assertIn("X2 = -0.67", salida)
        self.assertIn("X3 = 6.33", salida)
        self.assertIn("X4 = -3.67", salida)

    def test_sistema_con_filas_iguales(self):
        """Prueba con filas iguales (infinitas soluciones)"""
        mat = Matriz(2, 3)
        datos = [
            [1, 2, 3],
            [1, 2, 3]
        ]
        for i in range(2):
            for j in range(3):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("El sistema tiene infinitas soluciones", salida)

    def test_sistema_con_filas_proporcionales(self):
        """Prueba con filas proporcionales (infinitas soluciones)"""
        mat = Matriz(2, 3)
        datos = [
            [1, 2, 3],
            [2, 4, 6]
        ]
        for i in range(2):
            for j in range(3):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("El sistema tiene infinitas soluciones", salida)

    def test_sistema_incompatible_3x3(self):
        """Prueba con sistema 3x3 incompatible"""
        mat = Matriz(3, 4)
        datos = [
            [1, 2, 3, 6],
            [1, 2, 3, 7],  # Mismo lado izquierdo, diferente derecho
            [2, 4, 6, 12]
        ]
        for i in range(3):
            for j in range(4):
                mat.set(i+1, j+1, datos[i][j])
        salida = self._capturar_output(mat)
        self.assertIn("El sistema no tiene solución", salida)


if __name__ == "__main__":
    print("\n==============================")
    print("  Pruebas unitarias LINAL")
    print("==============================\n")
    unittest.main(verbosity=2)
