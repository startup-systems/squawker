from flask import Flask
from flask import g
from flask import render_template
from flask import request
import sqlite3
import time
import datetime
import random
import webbrowser

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


@app.route('/', methods=['GET', 'POST'])
def root():
    conn = get_db()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS allSquawksIEverMade(datestamp TEXT, squawk TEXT)')
    s = []
    c.execute('SELECT * FROM allSquawksIEverMade')
    for row in c.fetchall():
        s.append(row[1])
        t = []
        for i in reversed(s):
            t.append(i)
    return render_template('Homepage.html', s=t)


@app.route('/send', methods=['GET', 'POST'])
def send():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = str(request.form['squawk'])
        if len(data) > 140:
            s = []
            s.append('Error Code 400: Input correct form details')
            return render_template('Homepage.html', s=s)
        unix = time.time()
        timestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        c.execute("INSERT INTO allSquawksIEverMade (datestamp, squawk) VALUES (?, ?)", (timestamp, data))
        conn.commit()
        webbrowser.open('http://localhost:5000/')
        return 'all Ok'


if __name__ == '__main__':
    app.run()
