from flask import Flask, g, render_template, request, abort, redirect
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


def insert(str):
    if (len(str) > 140):
        abort(400)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mytable(str) VALUES ("{}")'.format(str))
    conn.commit()
    cursor.close()


def selectAll():
    conn = get_db()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM mytable").fetchall()
    cursor.close()
    return row[::-1]


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@app.route('/post', methods=['POST'])
def post():
    comment = request.form.get('comment')
    insert(comment)
    return redirect('/')


@app.route('/')
@app.route('/p/<int:page>', methods=['GET', 'POST'])
def root(page=1):
    res = selectAll()
    return render_template('index.html', greeting_list=res[(page - 1) * 20:min((page) * 20, len(res))], prev_num=page - 1, next_num=page + 1, lastpage=len(res) / 20, thisPage=page)


if __name__ == '__main__':
    app.run()
