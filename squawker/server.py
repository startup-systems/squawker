from flask import Flask, g, render_template, redirect, request, url_for, abort
import sqlite3
from math import ceil


# -- leave these lines intact --
app = Flask(__name__)


# Reference: http://flask.pocoo.org/snippets/44/
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
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


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

PER_PAGE = 10


# URL generation helper
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def get_current_page_feed(feeds, page):
    return feeds[((page - 1) * PER_PAGE):min(((page - 1) * PER_PAGE) + PER_PAGE, len(feeds))]


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page):
    conn = get_db()
    # TODO change this
    cursor_object = conn.execute('SELECT * FROM squawks ORDER BY post_time DESC')
    feeds = cursor_object.fetchall()
    count = len(feeds)
    feeds = get_current_page_feed(feeds, page)
    if not feeds and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('homepage.html', pagination=pagination, feeds=feeds)


@app.route('/new_sq', methods=['POST'])
def new_sq():
    db = get_db()
    new_sq = request.form['content']
    if len(new_sq) > 140:
        abort(400)
    db.execute('INSERT INTO squawks (feed) values (?)', [new_sq])
    db.commit()
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run()
