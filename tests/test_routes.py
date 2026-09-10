from models import Cliente, Producto, db


def test_index_muestra_estado_vacio(client):
    response = client.get('/')

    assert response.status_code == 200
    assert 'No hay productos registrados' in response.get_data(as_text=True)


def test_menu_permite_navegar_entre_productos_y_clientes(client):
    response = client.get('/')

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert 'Productos' in body
    assert 'Clientes' in body


def test_nuevo_producto_crea_registro_y_muestra_flash(client, app):
    response = client.post(
        '/producto/nuevo',
        data={
            'nombre': 'Laptop',
            'descripcion': 'Portatil de prueba',
            'precio': '1500.50',
            'cantidad': '4',
            'categoria': 'Electrónica',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'creado exitosamente' in response.get_data(as_text=True)

    with app.app_context():
        producto = Producto.query.filter_by(nombre='Laptop').one()
        assert producto.precio == 1500.5
        assert producto.cantidad == 4
        assert producto.categoria == 'Electrónica'


def test_nuevo_producto_rechaza_duplicados_insensibles(client, make_product, app):
    make_product(nombre='Laptop')

    response = client.post(
        '/producto/nuevo',
        data={
            'nombre': 'laptop',
            'descripcion': 'Duplicado',
            'precio': '999.99',
            'cantidad': '1',
            'categoria': 'Otros',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'ya existe en el sistema' in response.get_data(as_text=True)

    with app.app_context():
        assert Producto.query.count() == 1


def test_nuevo_producto_rechaza_datos_invalidos(client, app):
    response = client.post(
        '/producto/nuevo',
        data={
            'nombre': '',
            'descripcion': 'Inválido',
            'precio': '-1',
            'cantidad': '-3',
            'categoria': 'Otros',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'Por favor completa los campos requeridos correctamente' in response.get_data(as_text=True)


def test_editar_producto_actualiza_datos(client, make_product, app):
    producto = make_product(nombre='Laptop')

    response = client.post(
        f'/producto/{producto.id}/editar',
        data={
            'nombre': 'Laptop Pro',
            'descripcion': 'Actualizada',
            'precio': '1750.00',
            'cantidad': '6',
            'categoria': 'Electrónica',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'actualizado exitosamente' in response.get_data(as_text=True)

    with app.app_context():
        actualizado = db.session.get(Producto, producto.id)
        assert actualizado.nombre == 'Laptop Pro'
        assert actualizado.descripcion == 'Actualizada'
        assert actualizado.precio == 1750.0
        assert actualizado.cantidad == 6


def test_editar_producto_rechaza_nombre_duplicado(client, make_product, app):
    producto = make_product(nombre='Laptop')
    make_product(nombre='Monitor')

    response = client.post(
        f'/producto/{producto.id}/editar',
        data={
            'nombre': 'monitor',
            'descripcion': 'Intento duplicado',
            'precio': '1500.00',
            'cantidad': '2',
            'categoria': 'Otros',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'ya está siendo usado por otro producto' in response.get_data(as_text=True)

    with app.app_context():
        original = db.session.get(Producto, producto.id)
        assert original.nombre == 'Laptop'


def test_ver_producto_muestra_detalle(client, make_product):
    producto = make_product(nombre='Laptop')

    response = client.get(f'/producto/{producto.id}')

    assert response.status_code == 200
    assert 'Laptop' in response.get_data(as_text=True)
    assert 'Sin stock' not in response.get_data(as_text=True)


def test_eliminar_producto_borra_registro(client, make_product, app):
    producto = make_product(nombre='Laptop')

    response = client.post(f'/producto/{producto.id}/eliminar', follow_redirects=True)

    assert response.status_code == 200
    assert 'eliminado exitosamente' in response.get_data(as_text=True)

    with app.app_context():
        assert db.session.get(Producto, producto.id) is None


def test_index_paginaa_resultados(client, app):
    with app.app_context():
        for indice in range(12):
            db.session.add(
                Producto(
                    nombre=f'Producto {indice}',
                    precio=10 + indice,
                    cantidad=indice,
                    categoria='Otros',
                )
            )
        db.session.commit()

    response = client.get('/')

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'Producto 0' in body
    assert 'Producto 9' in body
    assert 'Producto 10' not in body


def test_clientes_muestra_estado_vacio(client):
    response = client.get('/clientes')

    assert response.status_code == 200
    assert 'No hay clientes registrados' in response.get_data(as_text=True)


def test_nuevo_cliente_crea_registro_y_muestra_flash(client, app):
    response = client.post(
        '/cliente/nuevo',
        data={
            'nombre': 'Ana Pérez',
            'email': 'ana@example.com',
            'telefono': '555-0101',
            'direccion': 'Calle 123',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'creado exitosamente' in response.get_data(as_text=True)

    with app.app_context():
        cliente = Cliente.query.filter_by(email='ana@example.com').one()
        assert cliente.nombre == 'Ana Pérez'
        assert cliente.telefono == '555-0101'
        assert cliente.direccion == 'Calle 123'


def test_nuevo_cliente_rechaza_correo_duplicado_insensible(client, make_client, app):
    make_client(email='ana@example.com')

    response = client.post(
        '/cliente/nuevo',
        data={
            'nombre': 'Ana Dos',
            'email': 'ANA@EXAMPLE.COM',
            'telefono': '555-0199',
            'direccion': 'Otra calle',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'ya existe en el sistema' in response.get_data(as_text=True)

    with app.app_context():
        assert Cliente.query.count() == 1


def test_nuevo_cliente_rechaza_datos_invalidos(client):
    response = client.post(
        '/cliente/nuevo',
        data={
            'nombre': '',
            'email': 'correo-invalido',
            'telefono': '',
            'direccion': '',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'Por favor completa los campos requeridos correctamente' in response.get_data(as_text=True)


def test_editar_cliente_actualiza_datos(client, make_client, app):
    cliente = make_client(nombre='Ana', email='ana@example.com')

    response = client.post(
        f'/cliente/{cliente.id}/editar',
        data={
            'nombre': 'Ana Gómez',
            'email': 'ana.gomez@example.com',
            'telefono': '555-0202',
            'direccion': 'Nueva dirección',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'actualizado exitosamente' in response.get_data(as_text=True)

    with app.app_context():
        actualizado = db.session.get(Cliente, cliente.id)
        assert actualizado.nombre == 'Ana Gómez'
        assert actualizado.email == 'ana.gomez@example.com'
        assert actualizado.telefono == '555-0202'
        assert actualizado.direccion == 'Nueva dirección'


def test_editar_cliente_rechaza_correo_duplicado(client, make_client, app):
    cliente = make_client(nombre='Ana', email='ana@example.com')
    make_client(nombre='Beto', email='beto@example.com')

    response = client.post(
        f'/cliente/{cliente.id}/editar',
        data={
            'nombre': 'Ana',
            'email': 'BETO@EXAMPLE.COM',
            'telefono': '555-0101',
            'direccion': 'Dirección base',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'ya está siendo usado por otro cliente' in response.get_data(as_text=True)

    with app.app_context():
        original = db.session.get(Cliente, cliente.id)
        assert original.email == 'ana@example.com'


def test_ver_cliente_muestra_detalle(client, make_client):
    cliente = make_client(nombre='Ana', email='ana@example.com')

    response = client.get(f'/cliente/{cliente.id}')

    assert response.status_code == 200
    assert 'Ana' in response.get_data(as_text=True)
    assert 'ana@example.com' in response.get_data(as_text=True)


def test_eliminar_cliente_borra_registro(client, make_client, app):
    cliente = make_client(nombre='Ana', email='ana@example.com')

    response = client.post(f'/cliente/{cliente.id}/eliminar', follow_redirects=True)

    assert response.status_code == 200
    assert 'eliminado exitosamente' in response.get_data(as_text=True)

    with app.app_context():
        assert db.session.get(Cliente, cliente.id) is None


def test_clientes_paginaa_resultados(client, app):
    with app.app_context():
        for indice in range(12):
            db.session.add(
                Cliente(
                    nombre=f'Cliente {indice}',
                    email=f'cliente{indice}@example.com',
                )
            )
        db.session.commit()

    response = client.get('/clientes')

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'Cliente 0' in body
    assert 'Cliente 9' in body
    assert 'Cliente 10' not in body


def test_api_productos_devuelve_lista_json(client, make_product):
    make_product(nombre='Laptop', categoria='Electrónica')
    make_product(nombre='Monitor', categoria='Otros')

    response = client.get('/api/productos')

    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, list)
    assert len(payload) == 2
    assert {item['nombre'] for item in payload} == {'Laptop', 'Monitor'}


def test_api_producto_devuelve_un_solo_registro(client, make_product):
    producto = make_product(nombre='Laptop')

    response = client.get(f'/api/producto/{producto.id}')

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['nombre'] == 'Laptop'
    assert payload['id'] == producto.id


def test_api_buscar_productos_filtra_por_nombre_y_categoria(client, make_product):
    make_product(nombre='Laptop Gamer', categoria='Electrónica')
    make_product(nombre='Laptop Oficina', categoria='Electrónica')
    make_product(nombre='Monitor', categoria='Otros')

    response = client.get('/api/productos/buscar?q=laptop&categoria=Electrónica')

    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload) == 2
    assert all('Laptop' in item['nombre'] for item in payload)


def test_error_404_renderiza_template(client):
    response = client.get('/ruta-que-no-existe')

    assert response.status_code == 404
    assert 'Página no encontrada' in response.get_data(as_text=True)


def test_error_500_renderiza_template(client, app, monkeypatch):
    def boom():
        raise RuntimeError('boom')

    monkeypatch.setitem(app.view_functions, 'index', boom)
    app.config['PROPAGATE_EXCEPTIONS'] = False

    response = client.get('/')

    assert response.status_code == 500
    assert 'Error interno del servidor' in response.get_data(as_text=True)