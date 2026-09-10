# 🛍️ Administrador de Productos v1

Una aplicación web moderna para gestionar productos, construida con Flask y SQLAlchemy.

## ✨ Características

- **CRUD Completo**: Crear, leer, actualizar y eliminar productos
- **Interfaz Amigable**: Diseño responsivo con Bootstrap 5
- **Base de Datos**: SQLite integrada con SQLAlchemy ORM
- **API REST**: Endpoints JSON para integración con otras aplicaciones
- **Búsqueda**: Buscar productos por nombre y categoría
- **Paginación**: Gestión eficiente de grandes catálogos
- **Validación**: Validación de datos en formularios

## 📋 Requisitos

- Python 3.8+
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd /workspaces/GH-300repo
```

### 2. Crear entorno virtual

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` si es necesario cambiar la configuración.

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📚 Uso

### Interfaz Web

Accede a `http://localhost:5000` en tu navegador para:

- **Ver Productos**: Lista completa con paginación
- **Crear Producto**: Agrega nuevos productos con detalles
- **Editar Producto**: Modifica información existente
- **Eliminar Producto**: Elimina productos no deseados
- **Ver Detalles**: Información completa de cada producto

### API REST

La aplicación también proporciona endpoints JSON:

#### Obtener todos los productos
```bash
curl http://localhost:5000/api/productos
```

#### Obtener un producto específico
```bash
curl http://localhost:5000/api/producto/1
```

#### Buscar productos
```bash
curl "http://localhost:5000/api/productos/buscar?q=laptop&categoria=Electrónica"
```

## 📁 Estructura del Proyecto

```
.
├── app.py                    # Aplicación principal Flask
├── models.py                 # Modelos de base de datos
├── config.py                 # Configuración de la app
├── requirements.txt          # Dependencias Python
├── .env.example             # Ejemplo de variables de entorno
├── .gitignore               # Archivos a ignorar en Git
├── templates/               # Plantillas HTML
│   ├── base.html           # Template base
│   ├── index.html          # Lista de productos
│   ├── nuevo_producto.html # Crear producto
│   ├── editar_producto.html # Editar producto
│   ├── ver_producto.html   # Detalles del producto
│   ├── 404.html            # Página no encontrada
│   └── 500.html            # Error del servidor
├── static/                  # Archivos estáticos
│   └── style.css           # Estilos CSS personalizados
└── productos.db            # Base de datos SQLite (se crea automáticamente)
```

## 🗄️ Modelo de Datos

### Tabla: Productos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| nombre | String | Nombre del producto |
| descripcion | Text | Descripción detallada |
| precio | Float | Precio del producto |
| cantidad | Integer | Cantidad en stock |
| categoria | String | Categoría del producto |
| fecha_creacion | DateTime | Fecha de creación |
| fecha_actualizacion | DateTime | Última actualización |
| activo | Boolean | Estado activo/inactivo |

## 🔧 Comandos Útiles

### Usar la consola Flask interactiva

```bash
flask shell
```

Dentro de la consola:
```python
from models import db, Producto

# Ver todos los productos
Producto.query.all()

# Crear un producto
p = Producto(nombre="Laptop", precio=999.99, cantidad=5)
db.session.add(p)
db.session.commit()

# Buscar por nombre
Producto.query.filter_by(nombre="Laptop").first()

# Actualizar
p.precio = 899.99
db.session.commit()

# Eliminar
db.session.delete(p)
db.session.commit()
```

## 📝 Categorías Disponibles

- Electrónica
- Ropa
- Alimentos
- Libros
- Otros

## 🎨 Personalización

### Cambiar Puerto

Edita el final de `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Cambiar puerto aquí
```

### Cambiar Base de Datos

En `.env`:
```
# PostgreSQL
DATABASE_URL=postgresql://usuario:password@localhost/productos

# MySQL
DATABASE_URL=mysql+pymysql://usuario:password@localhost/productos
```

## 🚨 Solución de Problemas

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Puerto 5000 en uso
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "sqlite3.OperationalError: unable to open database file"
Asegúrate de tener permisos de escritura en el directorio del proyecto.

## 📦 Dependencias

- **Flask**: Framework web micro
- **Flask-SQLAlchemy**: ORM para base de datos
- **Flask-Migrate**: Gestión de migraciones
- **python-dotenv**: Variables de entorno

## 🌐 Deployment

### En Heroku

1. Crear archivo `Procfile`:
```
web: gunicorn app:app
```

2. Agregar `gunicorn` a `requirements.txt`

3. Desplegar:
```bash
heroku create tu-app
git push heroku main
```

### En PythonAnywhere

1. Sube los archivos
2. Configura Virtual Environment
3. Crea Web App con Flask
4. Apunta a `app.py`

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Aplicación de administración de productos - 2024

---

¿Preguntas? ¡Abre un issue en el repositorio!
