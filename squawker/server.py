from flask import Flask, g, request, render_template, redirect, abort, url_for
import sqlite3
import time
import pdb

# -- leave these lines intact --
app = Flask(__name__)
PER_PAGE = 20
has_next = False
has_prev = False


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


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/')
@app.route('/<int:page>', methods=['GET', 'POST'])
def root(page=1):
    # pdb.set_trace()
    conn = get_db()
    c = conn.cursor()
    # TODO change this
    c.execute('SELECT COUNT(*) from squawker')
    num_squawks = c.fetchone()[0]

    squawker = conn.cursor().execute("\
                SELECT * \
                FROM squawker \
                ORDER BY id DESC \
                LIMIT (?) OFFSET (?)", (PER_PAGE, (page - 1) * PER_PAGE))
    if (num_squawks > PER_PAGE * page):
        num_squawks -= PER_PAGE
        has_next = True
    else:
        has_next = False
    if page > 1:
        has_prev = True
    else:
        has_prev = False
    return render_template('index.html', squawker=squawker, has_next=has_next, page=page, num_squawks=num_squawks, root=root)


@app.route("/api/squawk", methods=["POST"])
def receive_squawk():
    if ((request.form['squawk']) == "" or len(request.form['squawk']) > 140):
        abort(400)
    else:
        db_add_squawk(request.form['squawk'])
    return redirect("/")


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
