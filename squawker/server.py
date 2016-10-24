from flask import Flask, g, render_template, request, redirect, url_for, abort
import sqlite3
from datetime import datetime, timezone
import math

# -- leave these lines intact --
app = Flask(__name__)
FORMAT = "%Y-%m-%d %H:%M:%S"
PER_PAGE = 20


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


@app.route('/')
@app.route('/<cur_page>')
def root(cur_page=None):
    if cur_page is None:
        cur_page = 1

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM squawker ORDER BY ts DESC;")
    page_count = math.ceil(cur.fetchone()[0] / 20)
    print(page_count)

    items = _get_one_page(cur_page)

    return render_template('base.html', items=items, page=cur_page, page_count=page_count)


def _get_one_page(page):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT post, ts FROM squawker ORDER BY ts DESC LIMIT %d OFFSET %d;" % (
        PER_PAGE, (int(page) - 1) * PER_PAGE))
    items = cur.fetchall()
    _ = map(lambda r: (r[0], _convert_time(r[1])), items)
    return _


def _convert_time(ts):
    dt = datetime.strptime(ts, FORMAT)
    _ = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return _.strftime(FORMAT)


@app.route('/post', methods=["POST"])
def do_post():
    text = request.form['input-post']
    print(text)

    if is_valid(text):
        conn = get_db()
        cur = conn.cursor()
        stmt = 'INSERT INTO squawker (post) VALUES ("{0}");'.format(text)
        cur.execute(stmt)
        conn.commit()

        return redirect(url_for("root"))
    else:
        abort(400)


def is_valid(text):
    return 0 < len(text.rstrip()) <= 140


if __name__ == '__main__':
    app.run()
