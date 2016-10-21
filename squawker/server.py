import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# -- leave these lines intact --
app = Flask(__name__)
app.secret_key = 'b73730fa69991bf9e4702e49cec96c63' # Added by mw866


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
    db = get_db()
    # TODO change this
    cur = db.execute('select title, text from entries order by id desc')
    #entries = cur.fetchall()
    entries = [{"title" : row[0], "text" : row[1]} for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
