from flask import Flask, g, render_template, request
import sqlite3
import time

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

# this function from http://flask.pocoo.org/docs/0.11/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/', methods=['POST', 'GET'])
def root():
    conn = get_db()

    if request.method == 'POST':
        squawk_to_add = request.form['content']
        post_time = int(time.time())

        if len(squawk_to_add) > 140:
            return "Error: invalid input", 400

        insertion_query = "insert into squawks (id, create_time, squawk) values (?,?,?) "
                
        conn.cursor().execute(insertion_query, (1, post_time, squawk_to_add))
        conn.commit()
        
        list_of_squawks = []
        for squawk in query_db("select * from squawks order by create_time desc"):
            list_of_squawks.append(squawk[2])

        return render_template("front.html", squawks = list_of_squawks)

    list_of_squawks = []
    for squawk in query_db("select * from squawks"):
        list_of_squawks.append(squawk[2])

    return render_template("front.html", squawks = list_of_squawks)


if __name__ == '__main__':
    app.run()
