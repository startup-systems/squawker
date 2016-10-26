from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
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

def getSquawks():
    conn = get_db()
    res = conn.execute('Select * From squawks ORDER BY time desc')
    squawks = res.fetchall()
    return squawks
    
#@app.route('/', methods=['POST'])
def addSquawk():

    return render_template('index.html', squawks=squawks)#"Hello World!"
    #projectpath = request.form.projectFilePath

@app.route('/', methods=['POST'])
@app.route('/')
def root():    
    # TODO change this
    status = 200
    if request.method == 'POST':
        squawk = request.form['squawk']
        if (len(squawk) > 140):
            status = 400
            error = "greater than 140 characters"
        else:
            conn = get_db()
            conn.execute('INSERT INTO squawks (squawk) VALUES (?)', [squawk + str(i)])
            conn.commit()
        
    return render_template('index.html', squawks=getSquawks())#"Hello World!"

if __name__ == '__main__':
    app.run()
