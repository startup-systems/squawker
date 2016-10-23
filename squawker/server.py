from flask import Flask, g, request, render_template, url_for
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
# reference: http://flask.pocoo.org/docs/0.10/quickstart/#http-methods
# reference: https://docs.python.org/2/library/sqlite3.html
@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def root():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "POST":
        msg = request.form["squawkpost"]
        if len(msg) > 140:
            error = "You have to enter a shorter message"
            abort(400)
        else:
            cursor.execute("INSERT INTO table (\'message\') VALUES (\'" + msg + "\')")
            conn.commit()
            conn.close()
    cursor.execute("SELECT * FROM table ORDER BY time DESC")
    totalMsg = cursor.fetchall()
    return render_template("index.html", MSG=totalMsg)


if __name__ == '__main__':
    app.run()
