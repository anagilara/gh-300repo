# 🛠️ Guía de Desarrollo y Extensión

Esta guía te ayudará a extender y personalizar la aplicación de administración de productos.

## Estructura del Código

### `app.py` - Aplicación Principal
Contiene:
- Factory de aplicación Flask
- Rutas principales (CRUD)
- Endpoints de API REST
- Manejadores de errores

### `models.py` - Modelos de Base de Datos
Contiene:
- Modelo `Producto` con todas las propiedades
- Método `to_dict()` para convertir a JSON

### `config.py` - Configuración
Contiene:
- Configuración base
- Configuración de desarrollo
- Configuración de producción

## Agregar Nuevas Características

### 1. Agregar un Nuevo Campo al Producto

**En `models.py`:**
```python
class Producto(db.Model):
    # ... campos existentes ...
    sku = db.Column(db.String(50), unique=True)  # Nuevo campo
    proveedor = db.Column(db.String(200))        # Nuevo campo
```

**Crear migración:**
```bash
flask db migrate -m "Agregar campos sku y proveedor"
flask db upgrade
```

**En `templates/nuevo_producto.html` y `editar_producto.html`:**
```html
<div class="mb-3">
    <label for="sku" class="form-label">SKU</label>
    <input type="text" class="form-control" id="sku" name="sku">
</div>
```

**En `app.py`:**
```python
# En la ruta nuevo_producto()
sku = request.form.get('sku')
proveedor = request.form.get('proveedor')

producto = Producto(
    # ... otros campos ...
    sku=sku,
    proveedor=proveedor
)
```

---

### 2. Agregar Autenticación de Usuarios

**Instalar paquetes:**
```bash
pip install Flask-Login Flask-WTF
```

**Crear modelo de usuario en `models.py`:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

**Proteger rutas en `app.py`:**
```python
from flask_login import login_required, current_user

@app.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    # ... código existente ...
    pass
```

---

### 3. Agregar Sistema de Reportes

**Crear archivo `reports.py`:**
```python
from flask import jsonify
from models import db, Producto
from datetime import datetime, timedelta

def reporte_productos_sin_stock():
    """Productos con stock = 0"""
    productos = Producto.query.filter_by(cantidad=0).all()
    return [p.to_dict() for p in productos]

def reporte_productos_mas_vendidos(dias=30):
    """Top de productos (requiere campo de ventas)"""
    fecha_limite = datetime.now() - timedelta(days=dias)
    # Implementar lógica de ventas
    pass

def reporte_valor_inventario():
    """Valor total del inventario"""
    productos = Producto.query.all()
    total = sum(p.precio * p.cantidad for p in productos)
    return {'valor_total': total, 'productos': len(productos)}
```

**Agregar ruta en `app.py`:**
```python
from reports import reporte_valor_inventario

@app.route('/api/reportes/inventario')
def api_reporte_inventario():
    reporte = reporte_valor_inventario()
    return jsonify(reporte)
```

---

### 4. Agregar Validaciones Avanzadas

**Crear archivo `validators.py`:**
```python
from models import Producto

def validar_nombre_producto(nombre):
    """Valida que el nombre sea único y válido"""
    if not nombre or len(nombre) < 3:
        return False, "El nombre debe tener al menos 3 caracteres"
    
    if Producto.query.filter_by(nombre=nombre).first():
        return False, "El nombre ya existe"
    
    return True, "Válido"

def validar_precio(precio):
    """Valida que el precio sea positivo"""
    try:
        precio_float = float(precio)
        if precio_float < 0:
            return False, "El precio no puede ser negativo"
        return True, "Válido"
    except ValueError:
        return False, "El precio debe ser un número"

def validar_cantidad(cantidad):
    """Valida que la cantidad sea un entero no negativo"""
    try:
        cantidad_int = int(cantidad)
        if cantidad_int < 0:
            return False, "La cantidad no puede ser negativa"
        return True, "Válido"
    except ValueError:
        return False, "La cantidad debe ser un número entero"
```

---

### 5. Agregar Búsqueda Avanzada con Filtros

**En `app.py`:**
```python
@app.route('/api/productos/filtrar', methods=['GET'])
def api_filtrar_productos():
    """Filtrar productos con múltiples criterios"""
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    categoria = request.args.get('categoria')
    en_stock = request.args.get('en_stock', type=bool)
    
    query = Producto.query
    
    if precio_min:
        query = query.filter(Producto.precio >= precio_min)
    if precio_max:
        query = query.filter(Producto.precio <= precio_max)
    if categoria:
        query = query.filter_by(categoria=categoria)
    if en_stock:
        query = query.filter(Producto.cantidad > 0)
    
    productos = query.all()
    return jsonify([p.to_dict() for p in productos])
```

**Uso:**
```bash
curl "http://localhost:5000/api/productos/filtrar?precio_min=50&precio_max=200&categoria=Electrónica&en_stock=true"
```

---

### 6. Agregar Exportación de Datos

**Instalar paquetes:**
```bash
pip install openpyxl
```

**En `app.py`:**
```python
from flask import send_file
import openpyxl

@app.route('/exportar/excel')
def exportar_excel():
    """Exportar productos a Excel"""
    productos = Producto.query.all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"
    
    # Encabezados
    headers = ['ID', 'Nombre', 'Descripción', 'Precio', 'Cantidad', 'Categoría']
    ws.append(headers)
    
    # Datos
    for p in productos:
        ws.append([p.id, p.nombre, p.descripcion, p.precio, p.cantidad, p.categoria])
    
    # Guardar
    wb.save('productos.xlsx')
    return send_file('productos.xlsx', as_attachment=True)
```

---

### 7. Agregar Caché para Mejor Rendimiento

**Instalar Flask-Caching:**
```bash
pip install Flask-Caching
```

**En `app.py`:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/productos')
@cache.cached(timeout=300)  # Cache de 5 minutos
def api_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])
```

---

### 8. Agregar Logging

**En `app.py`:**
```python
import logging

# Configurar logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            # ... lógica ...
            logger.info(f'Producto creado: {nombre}')
        except Exception as e:
            logger.error(f'Error al crear producto: {str(e)}')
```

---

## Testing

**Crear archivo `test_app.py`:**
```python
import unittest
from app import app, db
from models import Producto

class TestProducto(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def test_crear_producto(self):
        response = self.app.post('/producto/nuevo', data={
            'nombre': 'Test Producto',
            'precio': '99.99',
            'cantidad': '10'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_listar_productos(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

**Ejecutar tests:**
```bash
python -m pytest test_app.py
```

---

## Mejores Prácticas

1. **Validar entrada**: Siempre valida datos del usuario
2. **Usar transacciones**: Asegura consistencia de datos
3. **Logging**: Registra eventos importantes
4. **Testing**: Escribe tests para nuevas funciones
5. **Documentación**: Mantén el código documentado
6. **Seguridad**: Usa HTTPS en producción
7. **Performance**: Usa índices en BD y caché

---

## Recursos Útiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [REST API Best Practices](https://restfulapi.net/)
