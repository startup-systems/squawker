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


@app.route('/', methods=["POST", "GET"])
def root():
    conn = get_db()
    c = conn.cursor()    
    if request.method == 'POST':
        newSquawk = request.form.get('content')
        # post length check
        if len(newSquawk) > 140:
            return "Input should be less than 140 characters!", 400
        else:
            query = "INSERT INTO squawks (squawk) VALUES (?)"
            c.execute(query, [newSquawk])
            conn.commit()
    # getting all the posts
    selectquery = "SELECT squawk FROM squawks order by id DESC"
    c.execute(selectquery)
    allSquawks = c.fetchall()
    c.close()
    return render_template("index.html", squawks=allSquawks)


if __name__ == '__main__':
    app.run()
