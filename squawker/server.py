import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


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

@app.route('/', methods=["POST", "GET"])
def root():
    conn = get_db()
    c = conn.cursor()
    if request.method == "POST":
        newPost = request.form["npost"]
        if len(newPost) > 140:
            abort(400)
        else:
            c.execute("INSERT INTO posts (msg) VALUES (?)", [newPost])
            conn.commit()
    c.execute("SELECT msg FROM posts ORDER BY id DESC")
    all_posts = c.fetchall()
    return render_template("index.html", allMsg=all_posts)



if __name__ == '__main__':
    app.run()
