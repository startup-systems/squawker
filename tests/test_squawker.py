import os
import pytest
import random
import re
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
    charset = string.ascii_letters + string.digits
    length = random.randint(5, 50)
    return ''.join(random.choice(charset) for _ in range(length))


def find_body_field(browser):
    field = browser.find_by_css('input[type="text"],textarea').first
    assert field is not None
    return field


def create_squawk(browser, body):
    url = '/'
    browser.visit(url)

    input_el = find_body_field(browser)
    input_el.fill(body)

    button = browser.find_by_css('input[type="submit"],button[type="submit"]').first
    assert button is not None
    button.click()


def has_any_attr(field, attrs):
    for attr in attrs:
        try:
            field[attr]
        except KeyError:
            continue
        else:
            return True
    return False


def test_response_code(test_app):
    response = test_app.get('/')
    assert response.status_code == 200


@pytest.mark.score(5)
def test_form_present(browser):
    url = '/'
    browser.visit(url)
    assert browser.is_element_present_by_tag('form')


@pytest.mark.score(20)
def test_all_squawks_present(browser):
    url = '/'

    num_squawks = random.randint(3, 9)
    bodies = [random_string() for _ in range(num_squawks)]
    for body in bodies:
        create_squawk(browser, body)

    # in case they didn't return to the homepage
    browser.visit(url)
    for body in bodies:
        assert browser.is_text_present(body)


@pytest.mark.score(20)
def test_reverse_chronological_order(browser):
    url = '/'

    num_squawks = random.randint(3, 9)
    bodies = ["Post {}".format(i) for i in range(num_squawks)]
    for body in bodies:
        create_squawk(browser, body)

    bodies.reverse()
    pattern = '.*'.join(bodies)

    browser.visit(url)

    assert re.search(pattern, browser.html, re.DOTALL + re.MULTILINE) is not None


@pytest.mark.score(30)
def test_create_squawk(browser):
    TEXT = random_string()
    create_squawk(browser, TEXT)
    assert browser.is_text_present(TEXT)


@pytest.mark.score(5)
def test_returns_to_homepage(browser):
    TEXT = random_string()
    create_squawk(browser, TEXT)
    assert browser.is_element_present_by_tag('form')


@pytest.mark.score(5)
def test_client_side_validation(browser):
    url = '/'
    browser.visit(url)
    field = find_body_field(browser)
    assert has_any_attr(field, ['maxlength', 'pattern']), "No HTML5 validation found."
