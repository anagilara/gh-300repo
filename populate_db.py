#!/usr/bin/env python3
"""
Script para generar datos de prueba en la aplicación de administración de productos
Ejecutar: python populate_db.py
"""

from app import app, db
from models import Producto

# Lista de productos de ejemplo
PRODUCTOS_EJEMPLO = [
    {
        'nombre': 'Laptop HP Pavilion',
        'descripcion': 'Laptop con procesador Intel Core i5, 8GB RAM, 256GB SSD',
        'precio': 599.99,
        'cantidad': 15,
        'categoria': 'Electrónica'
    },
    {
        'nombre': 'Mouse inalámbrico Logitech',
        'descripcion': 'Mouse inalámbrico con batería de 18 meses de duración',
        'precio': 29.99,
        'cantidad': 50,
        'categoria': 'Electrónica'
    },
    {
        'nombre': 'Teclado mecánico RGB',
        'descripcion': 'Teclado mecánico con iluminación RGB personalizable',
        'precio': 89.99,
        'cantidad': 25,
        'categoria': 'Electrónica'
    },
    {
        'nombre': 'Monitor 24" Full HD',
        'descripcion': 'Monitor LED IPS con resolución 1920x1080',
        'precio': 179.99,
        'cantidad': 12,
        'categoria': 'Electrónica'
    },
    {
        'nombre': 'Camiseta estampada',
        'descripcion': 'Camiseta de algodón 100% con estampado moderno',
        'precio': 19.99,
        'cantidad': 100,
        'categoria': 'Ropa'
    },
    {
        'nombre': 'Pantalón vaquero',
        'descripcion': 'Pantalón vaquero de alta calidad color azul oscuro',
        'precio': 49.99,
        'cantidad': 60,
        'categoria': 'Ropa'
    },
    {
        'nombre': 'Zapatillas deportivas',
        'descripcion': 'Zapatillas con excelente amortiguación y diseño moderno',
        'precio': 79.99,
        'cantidad': 40,
        'categoria': 'Ropa'
    },
    {
        'nombre': 'Café premium 1kg',
        'descripcion': 'Café arábica 100% grano entero, tostado fresco',
        'precio': 24.99,
        'cantidad': 80,
        'categoria': 'Alimentos'
    },
    {
        'nombre': 'Chocolate belga 200g',
        'descripcion': 'Chocolate belga oscuro con 70% cacao',
        'precio': 9.99,
        'cantidad': 150,
        'categoria': 'Alimentos'
    },
    {
        'nombre': 'Python Crash Course',
        'descripcion': 'Libro práctico para aprender Python desde cero',
        'precio': 39.99,
        'cantidad': 20,
        'categoria': 'Libros'
    },
    {
        'nombre': 'Clean Code',
        'descripcion': 'Guía completa para escribir código limpio y mantenible',
        'precio': 44.99,
        'cantidad': 15,
        'categoria': 'Libros'
    },
]

def populate_database():
    """Llena la base de datos con productos de ejemplo"""
    
    with app.app_context():
        # Verificar si ya hay productos
        if Producto.query.first():
            print("⚠️  La base de datos ya contiene productos. Abortando...")
            return
        
        print("🚀 Creando productos de ejemplo...")
        
        for i, prod_data in enumerate(PRODUCTOS_EJEMPLO, 1):
            producto = Producto(**prod_data)
            db.session.add(producto)
            print(f"   ✓ {i}. {prod_data['nombre']} - ${prod_data['precio']}")
        
        try:
            db.session.commit()
            total = Producto.query.count()
            print(f"\n✅ {total} productos creados exitosamente!")
            print("\nPuedes acceder a la aplicación en: http://localhost:5000")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al crear los productos: {str(e)}")

if __name__ == '__main__':
    populate_database()
