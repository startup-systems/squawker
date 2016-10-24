from flask import Flask, g, render_template, request, redirect, abort
import sqlite3
import time
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

ENTRIES_PER_PAGE = 20


def get_squawker_per_page(c, page):
    output = c.execute('SELECT * FROM squawker ORDER BY created_at DESC LIMIT ' + str(ENTRIES_PER_PAGE) + ' OFFSET ' + str(ENTRIES_PER_PAGE * (page - 1)))
    return output.fetchall()


def get_number_pages_of_squawker(c):
    output = c.execute('SELECT COUNT(*) FROM squawker')
    return ceil(int(output.fetchone()[0]) / ENTRIES_PER_PAGE)


@app.route('/', methods=["GET", "POST"], defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page):
    conn = get_db()
    c = conn.cursor()
    error = ""
    status = 200
    if request.method == "POST":
        if len(request.form["message"]) > 140:
            status = 400
            error = "The message must have 140 characters at most"
        else:
            c.execute("INSERT INTO squawker (message, created_at) VALUES ('" + request.form["message"] + "', " + str(int(time.time())) + ")")
            conn.commit()

    last_page = get_number_pages_of_squawker(c)
    if page < 1 or page > last_page:
        abort(404)

    squawkers = get_squawker_per_page(c, page)
    conn.close()
    return render_template('index.html', squawkers=squawkers, page=page, last_page=last_page, error=error), status


if __name__ == '__main__':
    app.run()
