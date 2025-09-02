from matriz import Matriz

import unittest

class TestMatriz(unittest.TestCase):
  def test_probar_limites(self):
    # Matriz para probar
    mat: Matriz = Matriz(3, 4)

    # todas estas deberian tirar un error
    # La posicion 3, 4 no existe
    self.assertRaises(Exception, mat.at, 3, 5)
    # Tampoco la posicion 4, 3
    self.assertRaises(Exception, mat.at, 4, 3)
    # o la posicion 0, 0
    self.assertRaises(Exception, mat.at, 0, 0)
    # o posiciones negativas
    self.assertRaises(Exception, mat.at, -1, 2)
    # Pero si 2,2 (y es 0, porque la matriz se inicializa en 0)
    self.assertEqual(mat.at(2,2), 0)

if __name__ == "__main__":
  # Corremos las pruebas
  unittest.main()