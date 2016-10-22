from flask import Flask, g, render_template, request, redirect, url_for, abort
import sqlite3
from math import ceil

# -- leave these lines intact --
app = Flask(__name__)


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


class Pagination(object):
    # Reference: http://flask.pocoo.org/snippets/44/

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
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

PER_PAGE = 20


def get_squawks_for_page(squawks, page):
    # return the squawks for the current page
    start_index = ((page - 1) * PER_PAGE)
    end_index = min(start_index + PER_PAGE, len(squawks))
    squawks = squawks[start_index:end_index]
    return squawks


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/', methods=["GET", "POST"], defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page):
    error = ""
    status = 200
    conn = get_db()
    if(request.method == "POST"):
        post_text = request.form['post_text']
        if len(post_text) > 140:
            status = 400
            error = "Error: Your post is too long! Keep to 140 characters, please."
        else:
            c = conn.execute('INSERT INTO squawks (text) VALUES (?)', [post_text])
            conn.commit()
    c = conn.execute('SELECT * FROM squawks ORDER BY id desc')
    squawks = c.fetchall()
    count = len(squawks)
    squawks = get_squawks_for_page(squawks, page)
    if not squawks and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('index.html', pagination=pagination, squawks=squawks, error=error), status


if __name__ == '__main__':
    app.run()
