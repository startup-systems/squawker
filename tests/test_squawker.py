import os
import pytest
import random
import re
from splinter import Browser
from squawker import server
import string
import tempfile
import time
from . import flaskclient_fix


URL = '/'
PAGE_SIZE = 20
# match case-insensitively
# http://stackoverflow.com/a/1625859/358804
NEXT_XPATH = "//a[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NEXT')]"


@pytest.fixture()
def db_fd():
    server.app.config['TESTING'] = True
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    return db_fd


@pytest.fixture()
def test_app(db_fd, request):
    client = server.app.test_client()
    with server.app.app_context():
        server.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(server.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


@pytest.fixture()
def browser(test_app):
    return Browser('flask', app=server.app)


def random_string(minlength=5, maxlength=40):
    charset = string.ascii_letters + string.digits
    length = random.randint(minlength, maxlength)
    return ''.join(random.choice(charset) for _ in range(length))


def find_body_field(browser):
    field = browser.find_by_css('input[type="text"],textarea').first
    assert field is not None
    return field


def create_squawk(browser, body):
    browser.visit(URL)

    input_el = find_body_field(browser)
    input_el.fill(body)

    button = browser.find_by_css('input[type="submit"],button[type="submit"]').first
    assert button is not None
    button.click()


def create_squawks(browser, count, delay=0):
    bodies = ["Post {}".format(i) for i in range(count)]
    for body in bodies:
        create_squawk(browser, body)
        if delay > 0:
            time.sleep(delay)

    return bodies


def test_response_code(test_app):
    response = test_app.get(URL)
    assert response.status_code == 200


@pytest.mark.score(5)
def test_form_present(browser):
    browser.visit(URL)
    assert browser.is_element_present_by_tag('form')


@pytest.mark.score(20)
def test_all_squawks_present(browser):
    num_squawks = random.randint(3, 9)
    bodies = create_squawks(browser, num_squawks)

    # in case they didn't return to the homepage
    browser.visit(URL)
    for body in bodies:
        assert browser.is_text_present(body)


@pytest.mark.score(20)
def test_reverse_chronological_order(browser):
    # the SQLite3 `datetime` type is down to the second by default, so wait between creating each squawk
    bodies = create_squawks(browser, 3, delay=1)

    bodies.reverse()
    pattern = '.*'.join(bodies)

    browser.visit(URL)

    assert re.search(pattern, browser.html, re.DOTALL + re.MULTILINE) is not None


@pytest.mark.score(30)
def test_create_squawk(browser):
    TEXT = random_string()
    create_squawk(browser, TEXT)
    browser.visit(URL)
    assert browser.is_text_present(TEXT)


@pytest.mark.score(5)
def test_returns_to_homepage(browser):
    TEXT = random_string()
    create_squawk(browser, TEXT)
    # the latter checks are needed because there seems to be a splinter(?) bug where it doesn't handle (certain?) redirects properly
    assert browser.is_element_present_by_tag('form') or (browser.status_code.code == 405 and browser.url == 'http://localhost/')


@pytest.mark.score(5)
def test_client_side_validation(browser):
    browser.visit(URL)
    assert browser.is_element_present_by_css('[maxlength="140"],[pattern]')


@pytest.mark.score(10)
def test_server_side_validation(browser):
    TEXT = random_string(minlength=141, maxlength=200)
    create_squawk(browser, TEXT)
    # TODO ignore if it's in the `value` of the `<input>`
    assert browser.is_text_not_present(TEXT)


@pytest.mark.score(5)
@pytest.mark.xfail
def test_page_size_limit(browser):
    bodies = create_squawks(browser, PAGE_SIZE + 1, delay=1)

    browser.visit(URL)
    assert browser.is_text_not_present(bodies[0])


@pytest.mark.score(5)
@pytest.mark.xfail
def test_next_only_present_for_pagination(browser):
    browser.visit(URL)
    assert browser.is_element_not_present_by_xpath(NEXT_XPATH), "`Next` link should not be present."

    create_squawks(browser, PAGE_SIZE + 1)

    browser.visit(URL)
    assert browser.is_element_present_by_xpath(NEXT_XPATH), "`Next` link should be present."


@pytest.mark.score(5)
@pytest.mark.xfail
def test_next_not_present_on_last_page(browser):
    bodies = create_squawks(browser, PAGE_SIZE + 1)

    browser.visit(URL)
    browser.find_by_xpath(NEXT_XPATH).first.click()

    assert browser.is_element_not_present_by_xpath(NEXT_XPATH), "`Next` link should not be present."


@pytest.mark.score(5)
@pytest.mark.xfail
def test_pagination(browser):
    bodies = create_squawks(browser, PAGE_SIZE + 1, delay=1)

    browser.visit(URL)
    browser.find_by_xpath(NEXT_XPATH).first.click()

    assert browser.is_text_present(bodies[0])
    assert browser.is_text_not_present(bodies[-1])
