from __future__ import print_function
from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import sys

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


@app.route('/')
def root(scroll=0):
    conn = get_db()
    cursor = conn.cursor()
    count = cursor.execute('SELECT COUNT(*) FROM squaks').fetchall()[0][0]
    print("count", count, file=sys.stderr)
    if request.args.get('scroll') is not None:
        scroll = int(request.args.get('scroll'))
        print("scroll", scroll, file=sys.stderr)
    else:
        scroll = 0
        print("No scrolling")
    if count:
        cursor.execute('SELECT * FROM squaks')
        squaks = list(reversed(cursor.fetchall()))
        print(squaks, scroll, file=sys.stderr)
        return render_template('index.html', squaks=squaks[scroll:scroll + 20], nextButton=(count > scroll + 20), scroll=scroll)
    else:
        return render_template('index.html', squaks=[], nextButton=False, scroll=0)


@app.route('/submit', methods=['POST'])
def newSquak():
    print(request.form['newSquak'], file=sys.stderr)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO squaks(squak) VALUES (?)', (request.form['newSquak'],))
    cur.execute('SELECT * from squaks')
    conn.commit()
    print(cur.fetchall(), file=sys.stderr)
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()
