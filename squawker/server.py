from flask import Flask, g, request, render_template, abort, redirect
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
def root():
    conn = get_db()
    c = conn.cursor()
    c.execute("Select msg from message order by id desc")
    result = c.fetchall()
    rows = []
    for r in result:
        rows.append(r[0])
    return render_template('index.html', rows=rows)


@app.route('/submitMessage', methods=['POST'])
def submitMessage():
    length = len(request.form['msg'])
    if length > 140:
        abort(400)
    else:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO message (msg) VALUES (?)", [request.form['msg']])
        conn.commit()
        conn.close()
    return redirect('/')
if __name__ == '__main__':
    app.run()
