from bs4 import BeautifulSoup
import os
import pytest
import random
from splinter import Browser
from squawker import server
import string
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


@pytest.fixture()
def browser(db_client):
    return Browser('flask', app=server.app)


def random_string():
    charset = string.ascii_uppercase + string.digits
    length = random.randint(5,50)
    return ''.join(random.choice(charset) for _ in range(length))


def create_squawk(browser, body):
    input_el = browser.find_by_css('input[type="text"],textarea').first
    assert input_el is not None
    input_el.fill(body)
    button = browser.find_by_css('input[type="submit"],button[type="submit"]').first
    button.click()


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
def test_create_squawk(browser):
    url = '/'
    browser.visit(url)

    TEXT = random_string()
    create_squawk(browser, TEXT)

    assert browser.is_text_present(TEXT)


@pytest.mark.score(20)
def test_all_squawks_present(browser):
    url = '/'

    bodies = [random_string() for _ in range(random.randint(3,9))]
    for body in bodies:
        browser.visit(url)
        create_squawk(browser, body)

    # don't assume they
    browser.visit(url)
    for body in bodies:
        assert browser.is_text_present(body)
