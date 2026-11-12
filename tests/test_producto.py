import io
import os
import sys
import unittest
from contextlib import redirect_stdout

# Permite importar el módulo desde src/ sin importar desde dónde se ejecuten las pruebas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from producto import Producto


def capturar_salida(producto):
    """Ejecuta mostrar_informacion() y devuelve lo que imprimió en pantalla."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        producto.mostrar_informacion()
    return buffer.getvalue()


class TestProducto(unittest.TestCase):

    def setUp(self):
        self.producto = Producto("P001", "Teclado", 350, 10)

    def test_cp01_crear_producto(self):
        """CP01 - Crear un producto con los datos proporcionados."""
        self.assertEqual(self.producto.codigo, "P001")
        self.assertEqual(self.producto.nombre, "Teclado")
        self.assertEqual(self.producto.precio, 350)
        self.assertEqual(self.producto.existencia, 10)

    def test_cp02_mostrar_codigo(self):
        """CP02 - Se muestra P001."""
        self.assertIn("P001", capturar_salida(self.producto))

    def test_cp03_mostrar_nombre(self):
        """CP03 - Se muestra Teclado."""
        self.assertIn("Teclado", capturar_salida(self.producto))

    def test_cp04_mostrar_precio(self):
        """CP04 - Se muestra 350."""
        self.assertIn("350", capturar_salida(self.producto))

    def test_cp05_mostrar_existencia(self):
        """CP05 - Se muestra 10."""
        self.assertIn("Existencia: 10", capturar_salida(self.producto))

    def test_cp06_mostrar_informacion_completa(self):
        """CP06 - Se muestran los cuatro datos correctamente."""
        salida = capturar_salida(self.producto)
        self.assertIn("Código: P001", salida)
        self.assertIn("Nombre: Teclado", salida)
        self.assertIn("Precio: $350", salida)
        self.assertIn("Existencia: 10", salida)

    def test_cp07_crear_otro_producto(self):
        """CP07 - Un segundo producto no se confunde con el primero."""
        mouse = Producto("P002", "Mouse", 180, 5)
        self.assertEqual(mouse.codigo, "P002")
        self.assertEqual(mouse.nombre, "Mouse")
        self.assertEqual(mouse.precio, 180)
        self.assertEqual(mouse.existencia, 5)
        # El primero sigue intacto
        self.assertEqual(self.producto.codigo, "P001")
        self.assertEqual(self.producto.nombre, "Teclado")
        salida_mouse = capturar_salida(mouse)
        self.assertIn("Mouse", salida_mouse)
        self.assertNotIn("Teclado", salida_mouse)


if __name__ == "__main__":
    unittest.main(verbosity=2)
