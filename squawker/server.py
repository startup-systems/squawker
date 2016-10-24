from flask import Flask, g, render_template, request
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
def root(page):
    error = ""
    status = 200
    conn = get_db()
    if(request.method == "POST"):
        post_text = request.form['post_text']
        if len(post_text) > 140:
            status = 400
            error = "Error! Your Tweet needs to be at most 140 characters!"
        else:
            c = conn.execute('INSERT INTO squawks (text) VALUES (?)', [post_text])
            conn.commit()
    c = conn.execute('SELECT * FROM squawks ORDER BY id desc')
    squawks = c.fetchall()
    count = len(squawks)
    squawks = get_squawks_for_page(squawks, page)
    if not squawks and page != 1:
        abort(404)
    return render_template('index.html', squawks=squawks, error=error), status


if __name__ == '__main__':
    app.run()
    app.run(host="0.0.0.0")
