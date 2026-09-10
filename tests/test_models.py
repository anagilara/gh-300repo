from datetime import datetime

from models import Cliente, Producto


def test_producto_repr():
    producto = Producto(nombre='Laptop', precio=1200.0)

    assert repr(producto) == '<Producto Laptop>'


def test_producto_to_dict_serializa_campos_clave():
    producto = Producto(
        id=1,
        nombre='Laptop',
        descripcion='Equipo de prueba',
        precio=1200.5,
        cantidad=3,
        categoria='Electrónica',
        activo=True,
    )
    producto.fecha_creacion = datetime(2026, 1, 2, 3, 4, 5)
    producto.fecha_actualizacion = datetime(2026, 1, 3, 4, 5, 6)

    assert producto.to_dict() == {
        'id': 1,
        'nombre': 'Laptop',
        'descripcion': 'Equipo de prueba',
        'precio': 1200.5,
        'cantidad': 3,
        'categoria': 'Electrónica',
        'activo': True,
        'fecha_creacion': '2026-01-02 03:04:05',
        'fecha_actualizacion': '2026-01-03 04:05:06',
    }


def test_cliente_repr():
    cliente = Cliente(nombre='Ana', email='ana@example.com')

    assert repr(cliente) == '<Cliente Ana>'


def test_cliente_to_dict_serializa_campos_clave():
    cliente = Cliente(
        id=1,
        nombre='Ana',
        email='ana@example.com',
        telefono='555-0101',
        direccion='Calle Falsa 123',
        activo=True,
    )
    cliente.fecha_creacion = datetime(2026, 1, 2, 3, 4, 5)
    cliente.fecha_actualizacion = datetime(2026, 1, 3, 4, 5, 6)

    assert cliente.to_dict() == {
        'id': 1,
        'nombre': 'Ana',
        'email': 'ana@example.com',
        'telefono': '555-0101',
        'direccion': 'Calle Falsa 123',
        'activo': True,
        'fecha_creacion': '2026-01-02 03:04:05',
        'fecha_actualizacion': '2026-01-03 04:05:06',
    }