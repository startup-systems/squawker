from flask import Flask, g, render_template, redirect, request, url_for, abort
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
    conn = get_db()
    # TODO change this
    cursor_object = conn.execute('SELECT * FROM squawks ORDER BY post_time DESC')
    feeds = cursor_object.fetchall()
    return render_template('homepage.html', feeds=feeds)


@app.route('/new_sq', methods=['POST'])
def new_sq():
    db = get_db()
    new_sq = request.form['content']
    if len(new_sq) > 140:
        abort(400)
    db.execute('INSERT INTO squawks (feed) values (?)', [new_sq])
    db.commit()
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run()
