from flask import Flask, g
import sqlite3
from flask import render_template, request, redirect, url_for, abort

# -- leave these lines intact --
app = Flask(__name__)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawks.db')
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


@app.route('/squawk/', methods=['POST'])
def squawk():
    s = request.form['squawkText']

    if s is None:
        return redirect(url_for('root'))

    if len(s) > 140:
        return "<h1>ERROR 400 BAD REQUEST</h1>"

    conn = get_db()
    cursor = conn.execute("INSERT INTO squawks (squawk) VALUES (?)", [s])
    conn.commit()
    conn.close()
    return redirect(url_for('root'))


@app.route('/')
def root():
    conn = get_db()
    cursor = conn.execute("SELECT id, squawk FROM squawks ORDER BY id desc")
    allRows = cursor.fetchall()

    return render_template("index.html", squawks=allRows)


if __name__ == '__main__':
    app.run()
