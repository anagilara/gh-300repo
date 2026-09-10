#!/bin/bash
# Guía rápida de inicio para la aplicación de administración de productos

echo "🚀 Iniciando configuración de la aplicación de administración de productos..."

# Crear entorno virtual
echo ""
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo ""
echo "✓ Entorno virtual creado"
echo "⚠️  Activa el entorno virtual ejecutando:"
echo "    source venv/bin/activate"

# Instalar dependencias
echo ""
echo "📥 Instalando dependencias (ejecuta esto después de activar venv)..."
echo "    pip install -r requirements.txt"

echo ""
echo "📝 Configurar variables de entorno:"
echo "    cp .env.example .env"

echo ""
echo "🗄️  Poblar base de datos con datos de ejemplo (opcional):"
echo "    python populate_db.py"

echo ""
echo "🌐 Ejecutar la aplicación:"
echo "    python app.py"

echo ""
echo "✅ Pasos completados. ¡Accede a http://localhost:5000 en tu navegador!"
