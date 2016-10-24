from flask import Flask, g
import sqlite3
import datetime

# -- leave these lines intact --
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

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
def show_entries():
    conn = get_db()
    cur = conn.execute('SELECT id, phrase, time FROM squawks ORDER BY time DESC')
    entries = cur.fetchall()

    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    text = request.form['text']
    if len(text)>140:
        abort(400)
        return
    db = get_db()
    db.execute('INSERT INTO squawks (phrase, time) VALUES (?, ?)', [text, datetime.datetime.utcnow()])
    db.commit()
    # flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
