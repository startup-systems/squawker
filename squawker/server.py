from flask import Flask, g, render_template, abort, request
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
    if (request.method == "POST"):
        message = request.form['message']
        if len(message) <= 140:
            cc_object = conn.execute('INSERT INTO squawks (message) VALUES (?)', [message])
            conn.commit()
        else:
            abort(400)

    cc_object = conn.execute('SELECT * FROM squawks ORDER BY timestamp desc')
    squawkers = cc_object.fetchall()

    return render_template('index.html', squawks=squawkers)


if __name__ == '__main__':
    app.run()
