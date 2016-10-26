from flask import Flask, g, jsonify
import sqlite3
from flask import render_template, request, redirect, url_for, abort
from math import ceil

app = Flask(__name__)

# set number of squawks per page
PER_PAGE = 20


# Set up and initialize db
def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker.db')
        g.sqlite_db = sqlite3.connect(db_name)

    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()
# ------------------------------


# pagination object from flask documentation
class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or (num > self.page - left_current - 1 and num < self.page + right_current) or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


# get squawks for page
def get_squawks_for_page(squawks_list, page, PER_PAGE):
    # iterate over squawks
    if (page == 1):
        i = 0
        j = 20
    else:
        i = ((page - 1) * PER_PAGE)
        j = page * PER_PAGE
    # get squawks for indicated page
    squawks = squawks_list[i:j]
    return squawks


# url generator
def url_for_pages(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_pages'] = url_for_pages


# main router
@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page, defaults=1):
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT ID, squawk_text from squawks order by id desc')
    # iterate over all squawks and store
    squawks_list = cursor_object.fetchall()

    count = len(squawks_list)
    squawks = get_squawks_for_page(squawks_list, page, PER_PAGE)
    if not squawks and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('index.html', pagination=pagination, squawks=squawks)


# add a squawk via post request
@app.route('/add_squawk', methods=['POST'])
def add_squawk():
    # server side validation of squawk length
    if len(request.form['squawk_text']) > 140:
        abort(400)
    # create db connection and store the squawk
    conn = get_db()
    conn.execute('INSERT INTO squawks (squawk_text) VALUES (?)', [request.form['squawk_text']])
    conn.commit()
    return redirect(url_for('root'))


# TODO create a JSON API that lists all possible squawks
@app.route('/api/squawks', methods=['GET'])
def list_squawks():
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT ID, squawk_text from squawks order by id desc')
    # iterate over all squawks and store
    squawks = cursor_object.fetchall()
    return jsonify(squawks)


if __name__ == '__main__':
    app.run()
