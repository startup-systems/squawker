from datetime import datetime
from flask import Flask, g, abort
from flask import render_template
from flask import request
from flask import redirect
import sqlite3
from types import *


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


@app.route('/', methods=['GET','POST'])
def root():
    conn = get_db()
    cursor = conn.cursor()
    # TODO change this
    if request.method == "POST":
        if len(request.form['squawk']) > 140: abort(400)
        time = datetime.now()
        cursor.execute("""INSERT INTO Squawks (name,squawk,time) VALUES (?,?,?);""",(request.form['name'],request.form['squawk'],time))
        conn.commit()
        return redirect('/')
    else:
        cursor.execute("""SELECT * FROM Squawks;""")
        old_squawks = cursor.fetchall()
        def byTime(squawk):
            return squawk[2]
        old_squawks = sorted(old_squawks, key=byTime, reverse=True)
        return render_template('index.html', squawks = old_squawks)


if __name__ == '__main__':
    app.run()
