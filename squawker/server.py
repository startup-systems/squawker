from flask import Flask, g, request, redirect, url_for, render_template
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
@app.route('/page/<int:page_id>', methods=['GET', 'POST'])
def root(page_id=1):
    status = 200
    conn = get_db()
    c = conn.cursor()
    query = "SELECT msg FROM squawkers ORDER BY created_time DESC"
    c.execute(query)
    squawkers = c.fetchall()
    conn.commit()
    conn.close()
    _start = (page_id - 1) * 20
    _end = min(len(squawkers), (page_id - 1) * 20 + 20)
    return render_template("index.html", num=_end - _start, page=page_id, msgs=squawkers[_start:_end]), status


@app.route('/post', methods=['POST'])
def post_squawker():
    error = None
    if request.method == 'POST':
        text = request.form['msg']
        if len(text) > 140:
            error = "squawke too long"
            abort(400)
        elif len(text) == 0:
            error = "squawke is empty"
            abort(400)
        else:
            conn = get_db()
            c = conn.cursor()
            c.execute('INSERT INTO squawkers (msg) VALUES (?)', [request.form['msg']])
            conn.commit()
            conn.close()
            return redirect(url_for('root'))

if __name__ == '__main__':
    app.run()
