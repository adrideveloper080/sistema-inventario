class Producto:
    def __init__(self, codigo, nombre, precio, existencia):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.existencia = existencia

    def mostrar_informacion(self):
        print(f"Código: {self.codigo}")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio}")
        print(f"Existencia: {self.existencia}")



if __name__ == "__main__":
    producto = Producto("P001", "Teclado", 350.00, 20)
    producto.mostrar_informacion()