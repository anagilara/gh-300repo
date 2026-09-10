# 🚀 INICIO RÁPIDO

Sigue estos pasos para ejecutar la aplicación de administración de productos en tu computadora.

## Paso 1: Preparar el Entorno Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

## Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask
- SQLAlchemy
- Flask-Migrate
- python-dotenv

## Paso 3: Configurar Variables de Entorno (Opcional)

```bash
cp .env.example .env
```

Por defecto usa SQLite local, no requiere configuración adicional.

## Paso 4: Crear la Base de Datos e Insertar Datos de Prueba

```bash
python populate_db.py
```

Esto creará 11 productos de ejemplo para empezar a usar la app.

## Paso 5: Ejecutar la Aplicación

```bash
python app.py
```

Verás algo como:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

## Paso 6: Acceder a la Aplicación

Abre tu navegador y ve a: **http://localhost:5000**

---

## ✅ Listo!

Ya tienes la aplicación ejecutándose. Ahora puedes:

- 📋 Ver todos los productos en la lista
- ➕ Crear nuevos productos
- ✏️ Editar productos existentes
- 🗑️ Eliminar productos
- 🔍 Usar la API REST en `/api/productos`

---

## Comandos Útiles

### Detener la aplicación
```
Presiona Ctrl+C en la terminal
```

### Acceder a la consola Flask
```bash
flask shell
```

Dentro de la consola:
```python
from models import db, Producto
# Ver todos
Producto.query.all()
# Crear uno
p = Producto(nombre="Test", precio=10)
db.session.add(p)
db.session.commit()
```

### Ver la base de datos
```bash
# Linux/Mac
sqlite3 productos.db

# Windows
sqlite3.exe productos.db

# Listar tablas
.tables

# Ver estructura
.schema productos
```

### Regenerar base de datos
```bash
# Eliminar
rm productos.db

# Recrear (sin datos)
python -c "from app import app; from models import db; app.app_context().push(); db.create_all()"

# O con datos de ejemplo
python populate_db.py
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
# Asegúrate de que el entorno virtual esté activado
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Luego instala las dependencias
pip install -r requirements.txt
```

### Error: "Address already in use"
El puerto 5000 ya está en uso. Opciones:
```bash
# Opción 1: Usar otro puerto
python -c "from app import app; app.run(port=5001)"

# Opción 2: Ver qué está usando el puerto
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### Error: "SQLite database is locked"
Cierra cualquier otra instancia de la aplicación y la consola Flask.

---

## 📁 Archivos Importantes

- `app.py` - Aplicación principal
- `models.py` - Modelos de base de datos
- `templates/` - Páginas HTML
- `static/style.css` - Estilos
- `productos.db` - Base de datos (se crea automáticamente)
- `README.md` - Documentación completa
- `API_GUIDE.md` - Guía de API REST
- `DEVELOPMENT.md` - Guía de desarrollo

---

## 📚 Próximos Pasos

1. **Explorar la interfaz**: Crea, edita y elimina productos
2. **Probar la API**: Usa curl o Postman para probar los endpoints
3. **Ver API_GUIDE.md**: Para ejemplos de uso de la API
4. **Ver DEVELOPMENT.md**: Para agregar nuevas características

---

## 📞 Ayuda

Si tienes problemas:
1. Revisa que Python 3.8+ esté instalado: `python --version`
2. Verifica que el entorno virtual esté activado
3. Comprueba que requirements.txt se instaló correctamente
4. Consulta la documentación completa en `README.md`

¡Listo para desarrollar! 🎉
