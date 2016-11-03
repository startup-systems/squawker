from flask import Flask, g, request, redirect, url_for, abort, render_template
import sqlite3
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
def root():
    db = get_db()
    # TODO change this
    cur = db.execute('SELECT id, squawk FROM entries ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    squawk = request.form['text']
    if len(squawk) > 140:
        abort(400)
        return
    db = get_db()
    db.execute('INSERT INTO entries (squawk) VALUES (?)', [squawk])
    db.commit()
    return redirect(url_for('/'))

if __name__ == '__main__':
    app.run()
