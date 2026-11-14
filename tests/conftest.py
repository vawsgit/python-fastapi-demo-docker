"""Fixtures that import the general variant's app with a chosen database.

`unit_app` swaps in an in-memory SQLite engine, so the unit tier needs no database.
`app_module` connects to the PostgreSQL that `make test-integration` starts on port 5433.
"""

import importlib
import os
import sys
import types
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

GENERAL = Path(__file__).resolve().parent.parent / "server" / "general"
TEST_DATABASE_URL = "postgresql://test:test@127.0.0.1:5433/bookstore"


def _import_app(connect=None):
    for name in [m for m in sys.modules if m == "app" or m.startswith("app.")]:
        sys.modules.pop(name)
    sys.path.insert(0, str(GENERAL))
    try:
        if connect is not None:
            sys.modules["app.connect"] = connect
        return importlib.import_module("app.main")
    finally:
        sys.path.remove(str(GENERAL))


@pytest.fixture
def unit_app():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    connect = types.ModuleType("app.connect")
    connect.engine = engine
    connect.db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return _import_app(connect)


@pytest.fixture
def app_module():
    os.environ.setdefault("DOCKER_DATABASE_URL", TEST_DATABASE_URL)
    module = _import_app()
    yield module
    module.Base.metadata.drop_all(bind=module.engine)
