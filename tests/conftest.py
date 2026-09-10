from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from app import create_app
from config import TestingConfig
from models import Cliente, Producto, db


@pytest.fixture()
def app(tmp_path):
    test_db_path = tmp_path / 'test_productos.db'
    TestingConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{test_db_path}"

    app = create_app('testing')
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def make_product(app):
    def _make_product(**overrides):
        data = {
            'nombre': 'Producto base',
            'descripcion': 'Descripcion base',
            'precio': 99.99,
            'cantidad': 10,
            'categoria': 'Otros',
        }
        data.update(overrides)

        producto = Producto(**data)
        db.session.add(producto)
        db.session.commit()
        return producto

    return _make_product


@pytest.fixture()
def make_client(app):
    def _make_client(**overrides):
        data = {
            'nombre': 'Cliente base',
            'email': 'cliente@example.com',
            'telefono': '555-0101',
            'direccion': 'Dirección base',
        }
        data.update(overrides)

        cliente = Cliente(**data)
        db.session.add(cliente)
        db.session.commit()
        return cliente

    return _make_client