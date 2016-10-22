from bs4 import BeautifulSoup
import os
import pytest
from splinter import Browser
from squawker import server
import tempfile


@pytest.fixture()
def db_fd():
    server.app.config['TESTING'] = True
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
def test_app(db_client):
    return server.app.test_client()


def test_response_code(test_app):
    response = test_app.get('/')
    assert response.status_code == 200


@pytest.mark.score(5)
def test_form_present(test_app):
    response = test_app.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    form = soup.find('form')
    assert form is not None


@pytest.mark.score(30)
def test_create_squawk(db_client):
    browser = Browser('flask', app=server.app)
    url = '/'
    browser.visit(url)

    TEXT = "splinter - python acceptance testing for web applications"
    input_el = browser.find_by_css('input[type="text"],textarea').first
    assert input_el is not None
    input_el.fill(TEXT)
    button = browser.find_by_css('input[type="submit"]').first
    button.click()

    assert browser.is_text_present(TEXT)
