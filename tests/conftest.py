from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_project.app import app
from fast_project.database import get_session
from fast_project.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_overrides():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overrides
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        table_registry.metadata.drop_all(engine)


@contextmanager
def db_time_context(*, model, time=datetime.now()):
    def fake_time_hook(mapper, conection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return db_time_context


@pytest.fixture
def user(session: Session):
    user = User(
        username='bob_bom_moço',
        email='bobbonzinho@gmail.com',
        password='bobaqui',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
