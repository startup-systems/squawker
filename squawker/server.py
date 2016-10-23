from flask import Flask, g, render_template, request, redirect
import sqlite3
from datetime import datetime

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
    s = "SELECT squawk from squawks order by submitdate desc"
    c.execute(s)
    #squawksstr = []
    allrows = c.fetchall()
    allsquawks = []
    for s in allrows:
        allsquawks.append(s[0])
    return render_template('home.html', allsquawks=allsquawks)


@app.route('/submitNewSquawk', methods=["POST"])
def submitNewSquawk():
    conn = get_db()
    c = conn.cursor()
    time = str(datetime.now())
    s = 'INSERT INTO squawks VALUES ("{}", "{}")'.format(time, str(request.form["squawk"]))     
    c.execute(s)
    conn.commit()
    conn.close()
    return redirect('/')



if __name__ == '__main__':
    app.run()
