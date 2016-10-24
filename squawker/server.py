from flask import Flask, g, abort, redirect, render_template, url_for, request
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


@app.route('/', methods=["GET", "POST"])
def root():
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        addSquawk = request.form['content']
        if len(addSquawk) > 140:
            abort(400)
        else:
            addition = conn.execute("INSERT INTO squawks (addSquawk) VALUES (?)", [addSquawk])
            conn.commit()
    conn.execute("SELECT* FROM squawks ORDER BY createTime DESC")
    listSq = cur.fetchall()
    return render_template("index.html", allSquawks = listSq)

if __name__ == '__main__':