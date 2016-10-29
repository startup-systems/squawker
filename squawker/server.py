from flask import Flask, g, request, render_template, redirect, abort
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

init_db()


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


def db_read_squawker():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM squawker ORDER BY id DESC")
    return cur.fetchall()


def db_add_squawk(squawk):
    cur = get_db().cursor()
    t = str(time.time())
    squawk_info = (t, squawk)
    cur.execute("INSERT INTO squawker VALUES (?, ?)", squawk_info)
    get_db().commit()


@app.route('/')
def root():
    conn = get_db()
    # TODO change this
    squawker = db_read_squawker()
    return render_template('index.html', squawker=squawker)


@app.route("/api/squawk", methods=["POST"])
def receive_squawk():
    print(request.form)
    if ((request.form['squawk']) == "" or len(request.form['squawk']) > 140):
        abort(400)
    else:
        db_add_squawk(request.form['squawk'])
    return redirect("/")


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
