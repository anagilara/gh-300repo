from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Producto, Cliente
from config import config
import os


def create_app(config_name='development'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar base de datos
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ===== RUTAS PRINCIPALES =====

    @app.route('/')
    def index():
        """Página principal - lista de productos"""
        page = request.args.get('page', 1, type=int)
        productos = Producto.query.paginate(page=page, per_page=10)
        return render_template('index.html', productos=productos)

    @app.route('/clientes')
    def clientes():
        """Página principal de clientes"""
        page = request.args.get('page', 1, type=int)
        clientes = Cliente.query.paginate(page=page, per_page=10)
        return render_template('clientes.html', clientes=clientes)

    def obtener_producto_o_404(id):
        """Obtener un producto por ID o devolver 404 si no existe"""
        return Producto.query.get_or_404(id)

    def obtener_cliente_o_404(id):
        """Obtener un cliente por ID o devolver 404 si no existe"""
        return Cliente.query.get_or_404(id)

    def email_cliente_es_valido(email):
        """Validación básica para email de cliente"""
        partes = email.split('@')
        return len(partes) == 2 and all(partes) and '.' in partes[1]

    @app.route('/producto/nuevo', methods=['GET', 'POST'])
    def nuevo_producto():
        """Crear un nuevo producto"""
        if request.method == 'POST':
            try:
                nombre = request.form.get('nombre', '').strip()
                descripcion = request.form.get('descripcion', '').strip()
                precio = float(request.form.get('precio'))
                cantidad = int(request.form.get('cantidad', 0))
                categoria = request.form.get('categoria', '').strip()

                # Validar datos
                if not nombre or precio < 0:
                    flash('Por favor completa los campos requeridos correctamente', 'error')
                    return redirect(url_for('nuevo_producto'))

                if cantidad < 0:
                    flash('La cantidad no puede ser negativa', 'error')
                    return redirect(url_for('nuevo_producto'))

                # Verificar si el producto ya existe (case-insensitive)
                producto_existente = Producto.query.filter(
                    Producto.nombre.ilike(nombre)
                ).first()

                if producto_existente:
                    flash(f'El producto "{nombre}" ya existe en el sistema', 'error')
                    return redirect(url_for('nuevo_producto'))

                producto = Producto(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    cantidad=cantidad,
                    categoria=categoria
                )

                db.session.add(producto)
                db.session.commit()

                flash(f'Producto "{nombre}" creado exitosamente', 'success')
                return redirect(url_for('index'))

            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear el producto: {str(e)}', 'error')
                return redirect(url_for('nuevo_producto'))

        return render_template('nuevo_producto.html')

    @app.route('/producto/<int:id>/editar', methods=['GET', 'POST'])
    def editar_producto(id):
        """Editar un producto existente"""
        producto = obtener_producto_o_404(id)

        if request.method == 'POST':
            try:
                nombre_nuevo = request.form.get('nombre', '').strip()
                descripcion = request.form.get('descripcion', '').strip()
                precio = float(request.form.get('precio'))
                cantidad = int(request.form.get('cantidad', 0))
                categoria = request.form.get('categoria', '').strip()

                if not nombre_nuevo or precio < 0:
                    flash('Por favor completa los campos requeridos correctamente', 'error')
                    return redirect(url_for('editar_producto', id=id))

                # Verificar si el nuevo nombre ya existe en otro producto (case-insensitive)
                if nombre_nuevo.lower() != producto.nombre.lower():
                    producto_duplicado = Producto.query.filter(
                        Producto.nombre.ilike(nombre_nuevo)
                    ).first()

                    if producto_duplicado:
                        flash(f'El nombre "{nombre_nuevo}" ya está siendo usado por otro producto', 'error')
                        return redirect(url_for('editar_producto', id=id))

                # Actualizar datos
                producto.nombre = nombre_nuevo
                producto.descripcion = descripcion
                producto.precio = precio
                producto.cantidad = cantidad
                producto.categoria = categoria

                db.session.commit()
                flash(f'Producto "{producto.nombre}" actualizado exitosamente', 'success')
                return redirect(url_for('ver_producto', id=id))

            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar el producto: {str(e)}', 'error')
                return redirect(url_for('editar_producto', id=id))

        return render_template('editar_producto.html', producto=producto)

    @app.route('/producto/<int:id>')
    def ver_producto(id):
        """Ver detalles de un producto"""
        producto = obtener_producto_o_404(id)
        return render_template('ver_producto.html', producto=producto)

    @app.route('/producto/<int:id>/eliminar', methods=['POST'])
    def eliminar_producto(id):
        """Eliminar un producto"""
        producto = obtener_producto_o_404(id)

        try:
            nombre_producto = producto.nombre
            db.session.delete(producto)
            db.session.commit()
            flash(f'Producto "{nombre_producto}" eliminado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar el producto: {str(e)}', 'error')

        return redirect(url_for('index'))

    @app.route('/cliente/nuevo', methods=['GET', 'POST'])
    def nuevo_cliente():
        """Crear un nuevo cliente"""
        if request.method == 'POST':
            try:
                nombre = request.form.get('nombre', '').strip()
                email = request.form.get('email', '').strip()
                telefono = request.form.get('telefono', '').strip()
                direccion = request.form.get('direccion', '').strip()

                if not nombre or not email or not email_cliente_es_valido(email):
                    flash('Por favor completa los campos requeridos correctamente', 'error')
                    return redirect(url_for('nuevo_cliente'))

                cliente_existente = Cliente.query.filter(
                    Cliente.email.ilike(email)
                ).first()

                if cliente_existente:
                    flash(f'El correo "{email}" ya existe en el sistema', 'error')
                    return redirect(url_for('nuevo_cliente'))

                cliente = Cliente(
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    direccion=direccion
                )

                db.session.add(cliente)
                db.session.commit()

                flash(f'Cliente "{nombre}" creado exitosamente', 'success')
                return redirect(url_for('clientes'))

            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear el cliente: {str(e)}', 'error')
                return redirect(url_for('nuevo_cliente'))

        return render_template('nuevo_cliente.html')

    @app.route('/cliente/<int:id>/editar', methods=['GET', 'POST'])
    def editar_cliente(id):
        """Editar un cliente existente"""
        cliente = obtener_cliente_o_404(id)

        if request.method == 'POST':
            try:
                nombre = request.form.get('nombre', '').strip()
                email_nuevo = request.form.get('email', '').strip()
                telefono = request.form.get('telefono', '').strip()
                direccion = request.form.get('direccion', '').strip()

                if not nombre or not email_nuevo or not email_cliente_es_valido(email_nuevo):
                    flash('Por favor completa los campos requeridos correctamente', 'error')
                    return redirect(url_for('editar_cliente', id=id))

                if email_nuevo.lower() != cliente.email.lower():
                    cliente_duplicado = Cliente.query.filter(
                        Cliente.email.ilike(email_nuevo)
                    ).first()

                    if cliente_duplicado:
                        flash(f'El correo "{email_nuevo}" ya está siendo usado por otro cliente', 'error')
                        return redirect(url_for('editar_cliente', id=id))

                cliente.nombre = nombre
                cliente.email = email_nuevo
                cliente.telefono = telefono
                cliente.direccion = direccion

                db.session.commit()
                flash(f'Cliente "{cliente.nombre}" actualizado exitosamente', 'success')
                return redirect(url_for('ver_cliente', id=id))

            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar el cliente: {str(e)}', 'error')
                return redirect(url_for('editar_cliente', id=id))

        return render_template('editar_cliente.html', cliente=cliente)

    @app.route('/cliente/<int:id>')
    def ver_cliente(id):
        """Ver detalles de un cliente"""
        cliente = obtener_cliente_o_404(id)
        return render_template('ver_cliente.html', cliente=cliente)

    @app.route('/cliente/<int:id>/eliminar', methods=['POST'])
    def eliminar_cliente(id):
        """Eliminar un cliente"""
        cliente = obtener_cliente_o_404(id)

        try:
            nombre_cliente = cliente.nombre
            db.session.delete(cliente)
            db.session.commit()
            flash(f'Cliente "{nombre_cliente}" eliminado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar el cliente: {str(e)}', 'error')

        return redirect(url_for('clientes'))

    # ===== API REST (JSON) =====

    @app.route('/api/productos')
    def api_productos():
        """Obtener lista de productos en JSON"""
        productos = Producto.query.all()
        return jsonify([p.to_dict() for p in productos])

    @app.route('/api/producto/<int:id>')
    def api_producto(id):
        """Obtener un producto específico en JSON"""
        producto = obtener_producto_o_404(id)
        return jsonify(producto.to_dict())

    @app.route('/api/productos/buscar', methods=['GET'])
    def api_buscar_productos():
        """Buscar productos por nombre o categoría"""
        query = request.args.get('q', '')
        categoria = request.args.get('categoria', '')

        consulta = Producto.query

        if query:
            consulta = consulta.filter(Producto.nombre.ilike(f'%{query}%'))

        if categoria:
            consulta = consulta.filter_by(categoria=categoria)

        productos = consulta.all()
        return jsonify([p.to_dict() for p in productos])

    # ===== MANEJO DE ERRORES =====

    @app.errorhandler(404)
    def not_found(error):
        """Página no encontrada"""
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Error interno del servidor"""
        db.session.rollback()
        return render_template('500.html'), 500

    # ===== CONTEXTO DE APLICACIÓN =====

    @app.shell_context_processor
    def make_shell_context():
        """Contexto para flask shell"""
        return {'db': db, 'Producto': Producto, 'Cliente': Cliente}

    return app


# Crear aplicación
app = create_app(os.getenv('FLASK_ENV', 'development'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
