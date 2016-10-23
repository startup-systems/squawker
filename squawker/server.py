from flask import Flask, g, render_template, request, flash, redirect, url_for, abort
from math import ceil
import sqlite3
import time
import unicodedata


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

#Obtained from http://flask.pocoo.org/snippets/44/
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
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

PER_PAGE = 20

# Limted to 20 for page
def get_squawks_for_page(entries, page, per_page):
    i = (page - 1) * PER_PAGE
    j = i + PER_PAGE
    squawk_entries = entries[i:j]
    return squawk_entries

# url generator obtained from http://flask.pocoo.org/snippets/44/
def url_for_pages(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_pages'] = url_for_pages


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page):
    conn = get_db()
    cur = conn.execute('select squawker from mytable order by id desc')
    entries = cur.fetchall()
    # delete unicode values
    entries = map(lambda x: unicodedata.normalize('NFKD', x[0]).encode('ascii', 'ignore'), entries)
    count = len(entries)
    squawks_entries = get_squawks_for_page(entries, page, PER_PAGE)
    print(squawks_entries)
    if not squawks_entries and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('home.html', pagination=pagination, squawks_entries=squawks_entries)



@app.route('/add_squawker', methods=['POST'])
def add_squawker():
    if len(request.form['squawker']) > 140:
        abort(400)
    db = get_db()
    db.execute('insert into mytable (squawker) values (?)',
               [request.form['squawker']])
    db.commit()
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()
