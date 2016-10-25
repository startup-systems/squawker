from flask import Flask, request, g, session, redirect, url_for, abort, render_template, flash
import sqlite3


# -- leave these lines intact --
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "super secret key"


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


@app.route('/', methods=['POST', 'GET'])
def root():
    conn = get_db()
    cur = conn.cursor()
    conts = cur.execute('SELECT posts From mytable ORDER BY ID DESC')
    posts = conts.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['POST', 'GET'])
def add_post():
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        apost = request.form['posts']
        if len(apost) > 140:
            abort(400)
        else:
            cur.execute('INSERT INTO mytable (posts) VALUES (?)', [apost])
            conn.commit()
            flash('Successfully posted')
    return redirect(url_for('root'))
 
if __name__ == '__main__':
    app.run()
