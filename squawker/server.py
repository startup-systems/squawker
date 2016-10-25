from flask import Flask, g, render_template, request, redirect, abort, url_for
import sqlite3


# -- leave these lines intact --
app = Flask(__name__)
app.secret_key = 'some_secret'


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
def root(post=0):
    if request.args.get('post') is not None:
        post = int(request.args.get('post'))
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM squawks")
    squawks = list(reversed(c.fetchall()))
    has_next = (len(squawks) > post + 20)
    return render_template('index.html', squawks=squawks[post:post + 20], post=post, has_next=has_next, total=len(squawks))


@app.route('/submit', methods=['POST'])
def submit():
    if len(request.form['squawk']) > 140:
        abort(400)
    else:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO squawks(message) VALUES (?)", (request.form['squawk'],))
        conn.commit()
        return redirect(url_for('root'))

if __name__ == '__main__':
    app.run()
