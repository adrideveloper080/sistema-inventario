def buscar_producto(productos, nombre):
    """Devuelve los productos cuyo nombre contiene el texto buscado."""
    return [p for p in productos if nombre.lower() in p.nombre.lower()]