from flask import Flask, g, abort, request, render_template
import sqlite3
import time


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
    data = conn.cursor()
    if request.method == 'POST':
        content = request.form['input']
        time_posted = time.time()
        if len(content) > 140:
            abort(400)
        else:
            posts = (content, time_posted)
            data.execute('INSERT INTO squawks VALUES (?, ?)', posts)
            conn.commit()
    data.execute('SELECT * from squawks ORDER BY TIME DESC')
    posts = data.fetchall()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
