from flask import Flask, g, render_template, request, abort
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
@app.route('/', methods=["GET", "POST"])
def root():
    conn = get_db()
    return "Hello World!"
    cur = conn.cursor()
    if request.method == 'Post':
        squawks = request.form["messages"]
        if len(squawks) > 140:
                abort(400)
                error = 'Squawks are limited to 140 characters'
        else:
                cur.execute("INSERT INTO squawker(squawks) VALUES(?) ", squawks)
                conn.commit()
    cur.execute("SELECT squawks FROM squawker ORDER BY time DESC")
    all_squawks = cur.fetchall()
    return render_template('index.html', squawks=all_squawks)

if __name__ == '__main__':
    app.run()
