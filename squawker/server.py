from flask import Flask, g
import sqlite3


# -- leave these lines intact --
app = Flask(__name__)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker.db')
        g.sqlite_db = sqlite3.connect(db_name)

    return g.sqlite_db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()
# ------------------------------

def init_db():
    with app.app_context():
        conn = get_db()
        c = conn.cursor()
        print("Creating database table(s), if they don't exist.")
        c.execute('CREATE TABLE IF NOT EXISTS users (id integer);')
        conn.commit()


@app.route('/')
def hello():
    conn = get_db()
    # ...
    return "Hello World!"


if __name__ == '__main__':
    init_db()
    app.run()
