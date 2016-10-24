from flask import Flask, g
from flask import request, redirect
from flask import render_template
from flask import Blueprint
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
# References:
# https://www.tutorialspoint.com/
# http://www.w3schools.com/
# https://www.sitepoint.com/basic-jquery-form-validation-tutorial/
# http://opentechschool.github.io/python-flask/core/form-submission.html


@app.route('/')
def root():
    db = get_db()
    cur = db.cursor()
    rows = cur.execute('SELECT comment FROM mytable ORDER BY tstamp DESC LIMIT 2000')
    rowList = []
    for row in rows:
        rowList.append(row[0])
        print(row[0])

    LIMIT = 5
    count = len(rowList)
    return render_template('index.html', rows=rowList)


@app.route('/posts', methods=['POST'])
def newComment():
    db = get_db()
    cur = db.cursor()

    text = request.form['comment']
    print(text)

    if(len(text) < 2) or (len(text) > 140):
        rows = cur.execute('SELECT comment FROM mytable ORDER BY tstamp DESC LIMIT 2000')
        rowList = []
        for row in rows:
            rowList.append(row[0])
        return render_template('index.html', rows=rowList), 400
    else:
        result = cur.execute("INSERT into mytable(comment) VALUES (?)", (text,))
        db.commit()
        rows = cur.execute('SELECT comment FROM mytable ORDER BY tstamp DESC LIMIT 2000')
        rowList = []
        for row in rows:
            rowList.append(row[0])
        return render_template('index.html', rows=rowList)


if __name__ == '__main__':
    app.run()
