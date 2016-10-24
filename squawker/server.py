import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

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


@app.route('/', methods=["GET", "POST"])
def root():
    conn = get_db()
    if request.method == "POST":
        content = request.form['squawker_post']
        if len(content) > 140:
            abort(400)
        else:
            req = conn.execute('INSERT INTO squawks (text) VALUES (?)', [content])
            conn.commit()
    req2 = conn.execute('SELECT * FROM squawks ORDER BY timestamp desc')
    allSquawks = req2.fetchall()
    return render_template('index.html', squawkers=allSquawks)


if __name__ == '__main__':
    app.run()
