import pytest
from squawker import server


@pytest.fixture()
def app():
    server.app.config['TESTING'] = True
    return server.app.test_client()


def test_response_code(app):
    response = app.get('/')
    assert response.status_code == 200
