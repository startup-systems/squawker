from flask import Flask, g, render_template
import sqlite3
from datetime import datetime, timezone

# -- leave these lines intact --
app = Flask(__name__)
FORMAT = "%Y-%m-%d %H:%M:%S"


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
def root():
    # conn = get_db()
    # TODO

    items = _get_all_post()

    return render_template('base.html', items=items, page=1)


def _get_all_post():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT post, ts FROM squawker ORDER BY ts;")
    items = cur.fetchall()
    map(lambda r: (r[0], _convert_time(r[1])), items)
    return items


def _convert_time(ts):
    dt = datetime.strptime(ts, FORMAT)
    _ = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return _.strftime(FORMAT)


@app.route('/post')
def do_post():
    pass


if __name__ == '__main__':
    app.run()
