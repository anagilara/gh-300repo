from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Producto(db.Model):
    """Modelo para la tabla de productos"""
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    def to_dict(self):
        """Convierte el producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'categoria': self.categoria,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_actualizacion': self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S')
        }
