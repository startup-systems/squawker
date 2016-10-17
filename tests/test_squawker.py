import os
import pytest
from squawker import server
import tempfile


@pytest.fixture()
def db_fd():
    print("creating database")
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    return db_fd

@pytest.fixture()
def app(db_fd):
    return server.app.test_client()


def setup_method(self, method):
    server.app.config['TESTING'] = True

def teardown_method(self, method):
    os.close(self.db_fd)
    os.unlink(server.app.config['DATABASE'])

def test_response_code(app):
    response = app.get('/')
    assert response.status_code == 200
