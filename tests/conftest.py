import os
import tempfile
import pytest
from project_manager.app import app as flask_app # Corrected import
from project_manager.app import init_db # Assuming init_db is in project_manager.app

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    flask_app.config.update({
        "TESTING": True,
        "DATABASE": db_path,
    })

    with flask_app.app_context():
        init_db() # Initialize the schema for the test database

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
