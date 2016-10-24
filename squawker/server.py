import os
from flask import Flask, g, render_template, flash, request, redirect, url_for
import sqlite3


# -- leave these lines intact --
app = Flask(__name__)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


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
    db = get_db()
    cur = db.execute('select title, text from squawks')
    squawks = cur.fetchall()
    return render_template('squawks.html', entries=squawks)


@app.route('/addsquawk', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into squawks (title, text) values (?,?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfuly posted')
    return redirect_for(url_for('tweet'))


if __name__ == '__main__':
    app.run()
