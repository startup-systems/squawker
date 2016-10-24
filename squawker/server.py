from flask import Flask, g
from flask import request, redirect
from flask import render_template, url_for
from math import ceil
import sqlite3


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
# References:
# https://www.tutorialspoint.com/
# http://www.w3schools.com/
# https://www.sitepoint.com/basic-jquery-form-validation-tutorial/
# http://opentechschool.github.io/python-flask/core/form-submission.html
# http://flask.pocoo.org/snippets/44/



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


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page):
    db = get_db()
    cur = db.cursor()
    rows = cur.execute('SELECT comment FROM mytable ORDER BY tstamp DESC LIMIT 2000')
    rowList = []
    for row in rows:
        rowList.append(row[0])
        print(row[0])

    PER_PAGE = 20
    count = len(rowList)
    start = (page - 1) * 20
    end = start + 20
    users = rowList[start:end]
    pagination = Pagination(page, PER_PAGE, count)

    if not users and page != 1:
        abort(404)
    return render_template('index.html', rows=users, pagination=pagination)



@app.route('/posts', methods=['POST'])
def newComment():
    db = get_db()
    cur = db.cursor()

    text = request.form['comment']
    print(text)

    if(len(text) < 2) or (len(text) > 140):
        rows = cur.execute('SELECT comment FROM mytable ORDER BY tstamp DESC LIMIT 2000')
        rowList = []
        for row in rows:
            rowList.append(row[0])
        return redirect(url_for('root')), 400
    else:
        result = cur.execute("INSERT into mytable(comment) VALUES (?)", (text,))
        db.commit()
        rows = cur.execute('SELECT comment FROM mytable ORDER BY tstamp DESC LIMIT 2000')
        rowList = []
        for row in rows:
            rowList.append(row[0])
        return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()
