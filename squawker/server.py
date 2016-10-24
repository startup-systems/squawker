import sqlite3
import os
from flask import Flask, request, g, abort, render_template
import datetime

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


@app.route('/', methods=['POST', 'GET'])
def root():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "POST":
        msg = request.form["content"]
        if len(msg) <= 140:
            query = "INSERT INTO squawks (squawk, time_stamp) VALUES (?, ?)"
            time = datetime.datetime.now()
            cursor.execute(query, (msg, time))
            conn.commit()
        else:
            abort(400)
    cursor.execute("SELECT squawk FROM squawks ORDER BY time_stamp DESC")
    res = cursor.fetchall()
    return render_template("index.html", squawks=res)


if __name__ == '__main__':
    app.run()
