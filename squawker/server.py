from flask import Flask, g, render_template, request, redirect, url_for
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

# Add posts
def addPost(data):  
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO squawks (body) VALUES(?)", (data,))
    conn.commit()

def getPosts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT id, body FROM
                    squawks
                    ORDER BY id DESC """)
    temp = cur.fetchall()
    data = []
    idx = []
    cur.close()
    return temp

# Routes

# Index
@app.route('/')  
def root():
    squawks = getPosts()
    return render_template('index.html', squawks=squawks)

@app.route('/add/', methods=['POST'])  # Add
def add():
    # Check if post is 140 characters
    if (len(request.form["new_body"]) > 140):  
        return abort(400)
    addPost(request.form["new_body"])
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()
