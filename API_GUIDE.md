# 📡 API REST - Guía de Endpoints

Esta aplicación proporciona una API REST para trabajar con productos. Aquí se detallan todos los endpoints disponibles.

## Base URL
```
http://localhost:5000
```

## Endpoints de API

### 1. Obtener todos los productos

**GET** `/api/productos`

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Laptop HP",
    "descripcion": "Laptop con procesador Intel",
    "precio": 599.99,
    "cantidad": 15,
    "categoria": "Electrónica",
    "activo": true,
    "fecha_creacion": "2024-01-15 10:30:00",
    "fecha_actualizacion": "2024-01-15 10:30:00"
  },
  ...
]
```

**Ejemplo con curl:**
```bash
curl http://localhost:5000/api/productos
```

**Ejemplo con Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/productos')
productos = response.json()
print(productos)
```

---

### 2. Obtener un producto específico

**GET** `/api/producto/<id>`

**Parámetros URL:**
- `id` (integer, requerido): ID del producto

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Laptop HP",
  "descripcion": "Laptop con procesador Intel",
  "precio": 599.99,
  "cantidad": 15,
  "categoria": "Electrónica",
  "activo": true,
  "fecha_creacion": "2024-01-15 10:30:00",
  "fecha_actualizacion": "2024-01-15 10:30:00"
}
```

**Ejemplo con curl:**
```bash
curl http://localhost:5000/api/producto/1
```

**Ejemplo con Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/producto/1')
producto = response.json()
print(producto)
```

---

### 3. Buscar productos

**GET** `/api/productos/buscar`

**Parámetros Query:**
- `q` (string, opcional): Buscar por nombre
- `categoria` (string, opcional): Filtrar por categoría

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Laptop HP Pavilion",
    "descripcion": "Laptop con procesador Intel Core i5",
    "precio": 599.99,
    "cantidad": 15,
    "categoria": "Electrónica",
    "activo": true,
    "fecha_creacion": "2024-01-15 10:30:00",
    "fecha_actualizacion": "2024-01-15 10:30:00"
  }
]
```

**Ejemplos:**

```bash
# Buscar por nombre
curl "http://localhost:5000/api/productos/buscar?q=laptop"

# Filtrar por categoría
curl "http://localhost:5000/api/productos/buscar?categoria=Electrónica"

# Buscar con ambos parámetros
curl "http://localhost:5000/api/productos/buscar?q=laptop&categoria=Electrónica"
```

**Ejemplo con Python:**
```python
import requests

# Buscar por nombre
params = {'q': 'laptop'}
response = requests.get('http://localhost:5000/api/productos/buscar', params=params)
productos = response.json()
print(productos)

# Buscar con múltiples parámetros
params = {'q': 'laptop', 'categoria': 'Electrónica'}
response = requests.get('http://localhost:5000/api/productos/buscar', params=params)
productos = response.json()
print(productos)
```

---

## Ejemplos Avanzados

### Ejemplo 1: Obtener todos los productos de una categoría

```python
import requests

def obtener_productos_por_categoria(categoria):
    response = requests.get(
        'http://localhost:5000/api/productos/buscar',
        params={'categoria': categoria}
    )
    return response.json()

# Usar
productos_electronica = obtener_productos_por_categoria('Electrónica')
for producto in productos_electronica:
    print(f"{producto['nombre']} - ${producto['precio']}")
```

### Ejemplo 2: Buscar productos baratos

```python
import requests

def obtener_productos_baratos(max_precio):
    response = requests.get('http://localhost:5000/api/productos')
    productos = response.json()
    return [p for p in productos if p['precio'] <= max_precio]

# Usar
productos_baratos = obtener_productos_baratos(50)
for producto in productos_baratos:
    print(f"{producto['nombre']} - ${producto['precio']}")
```

### Ejemplo 3: Estadísticas de productos

```python
import requests
from statistics import mean, stdev

def estadisticas_productos():
    response = requests.get('http://localhost:5000/api/productos')
    productos = response.json()
    
    precios = [p['precio'] for p in productos]
    cantidades = [p['cantidad'] for p in productos]
    
    return {
        'total_productos': len(productos),
        'precio_promedio': mean(precios),
        'precio_minimo': min(precios),
        'precio_maximo': max(precios),
        'stock_total': sum(cantidades),
        'categorias': list(set(p['categoria'] for p in productos if p['categoria']))
    }

# Usar
stats = estadisticas_productos()
print(f"Total de productos: {stats['total_productos']}")
print(f"Precio promedio: ${stats['precio_promedio']:.2f}")
print(f"Stock total: {stats['stock_total']} unidades")
print(f"Categorías: {', '.join(stats['categorias'])}")
```

### Ejemplo 4: Integración con JavaScript/AJAX

```javascript
// Obtener todos los productos
fetch('/api/productos')
    .then(response => response.json())
    .then(productos => {
        productos.forEach(producto => {
            console.log(`${producto.nombre} - $${producto.precio}`);
        });
    });

// Buscar productos
fetch('/api/productos/buscar?q=laptop&categoria=Electrónica')
    .then(response => response.json())
    .then(productos => {
        console.log(`Se encontraron ${productos.length} productos`);
    });

// Obtener un producto específico
fetch('/api/producto/1')
    .then(response => response.json())
    .then(producto => {
        console.log(`${producto.nombre} - $${producto.precio}`);
        console.log(`Stock: ${producto.cantidad}`);
    });
```

---

## Códigos de Respuesta

| Código | Significado |
|--------|------------|
| 200 | Solicitud exitosa |
| 404 | Recurso no encontrado |
| 500 | Error interno del servidor |

---

## Notas Importantes

- Todos los endpoints retornan JSON
- No hay autenticación requerida en esta versión (solo para desarrollo)
- La búsqueda es insensible a mayúsculas/minúsculas
- Los precios se muestran con hasta 2 decimales
- Las fechas están en formato ISO 8601 (YYYY-MM-DD HH:MM:SS)

---

## Para Agregar Autenticación (Opcional)

Si deseas agregar autenticación, puedes usar Flask-HTTPAuth:

```bash
pip install Flask-HTTPAuth
```

Luego modifica `app.py` para agregar protección a los endpoints que lo requieran.
