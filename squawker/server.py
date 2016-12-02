from flask import Flask, g, jsonify, render_template, request, redirect, url_for, abort
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
# ---Methods----#


def getPosts(page=0):  # Grab posts
    conn = get_db()
    cur = conn.cursor()
    if (page):  # Paginate posts by 20
        offset = (page - 1) * 20
        cur.execute("""SELECT id, body FROM
                        squawks
                        ORDER BY id DESC
                        LIMIT 20 OFFSET (?)""", (offset, ))
    else:  # Get all posts
        cur.execute("""SELECT id, body FROM
                        squawks
                        ORDER BY id DESC """)
    temp = cur.fetchall()
    data = []
    idx = []
    cur.close()
    return temp


def addPost(data):  # Add posts
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO squawks (body) VALUES(?)", (data,))
    conn.commit()

# ---- Routes  ---- #


@app.route('/')  # Index
def root():
    return page()


@app.route('/<int:pageNum>')  # Pages
def page(pageNum=1):
    squawks = getPosts(pageNum)
    if(len(squawks) == 0 or squawks[len(squawks) - 1][0] == 1):
        last = True
    else:
        last = False
    # TODO change this
    return render_template('index.html', squawks=squawks, currPage=pageNum, last=last)


@app.route('/all')  # All Posts
def allPosts():
    squawks = getPosts()
    # TODO change this
    return render_template('index.html', squawks=squawks, currPage=1, last=True)


@app.route('/add/', methods=['POST'])  # Add
def add():
    if (len(request.form["new_body"]) > 140):  # Check length of post
        return abort(400)
    addPost(request.form["new_body"])
    return redirect(url_for('root'))


@app.route('/next/', methods=['GET'])  # Next
def nextPage():
    pageNum = int(request.path[1:])
    return redirect(url_for('page'), pageNum=pageNum)


if __name__ == '__main__':
    app.run()

# Sources:
# http://stackoverflow.com/questions/109232/what-is-the-best-way-to-paginate-results-in-sql-server
