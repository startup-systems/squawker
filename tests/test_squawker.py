import os
import pytest
from squawker import server
import tempfile


@pytest.fixture()
def db_fd():
    server.app.config['TESTING'] = True
    print("creating database")
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    return db_fd

@pytest.fixture()
def db_client(db_fd, request):
    client = server.app.test_client()
    with server.app.app_context():
        server.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(server.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client

@pytest.fixture()
def app(db_client):
    return server.app.test_client()


def test_response_code(app):
    response = app.get('/')
    assert response.status_code == 200
