from flask import Flask, g
import sqlite3


# -- leave these lines intact --

from flask import render_template, request, redirect, url_for

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
    db = get_db()
    squa = db.execute('select text from squawks order by id desc')
    squawks = squa.fetchall()
    return render_template('index.html', squawks=squawks)

@app.route('/post', methods=['POST'])
def add_squawk():
    # if not session.get('logged_in'):
    #     abort(400)
    db = get_db()
    db.execute('insert into squawks (text) values (?)',
                 [request.form['squawk_text']])
    db.commit()
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()
