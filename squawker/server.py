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


@app.route('/', methods=["GET", "POST"])
def root():
    conn = get_db()
    if request.method == "POST":
        getContent = request.form['squawker_info']
        if len(getContent) > 140:
            abort(400)
        else:
            c_object = conn.execute('INSERT INTO mytable (content) VALUES (?)', [getContent])
            conn.commit()
    cc_object = conn.execute('SELECT * FROM mytable ORDER BY timestamp desc')
    squawkers = cc_object.fetchall()
    # TODO change this
    return render_template('homepage.html', squawkers=squawkers)


if __name__ == '__main__':
    app.run()
