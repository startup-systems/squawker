from flask import Flask, g, request
import datetime
import sqlite3
import time
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('squawker', 'templates'))


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


@app.route('/', methods=['GET'])
def root():
    return get_homepage()


@app.route('/', methods=['POST'])
def createSquawk():
    if isValidSquawkForm(request.form):
        squawk = {
            'text': request.form['text'],
            'time': time.time(),
            'username': 'trvslhlt'
        }
        create_squawk(squawk)
        return get_homepage()
    else:
        return '', 400


def get_homepage():
    squawks = get_all_squawks()
    template = env.get_template('index.html')
    return template.render(squawks=squawks)


def create_squawk(data):
    db = get_db()
    c = db.cursor()
    squawk = (data['time'], data['username'], data['text'])
    c.execute('INSERT INTO squawks(time, username, text) VALUES (?, ?, ?)', squawk)
    db.commit()


def get_all_squawks():
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM squawks ORDER BY TIME DESC')
    all_rows = c.fetchall()
    squawks = [marshal_squawk_row(row) for row in all_rows]
    return squawks


def marshal_squawk_row(row):
    time = datetime.datetime.fromtimestamp(int(row[1]))
    pretty_time = time.strftime('%Y/%m/%d %H:%M:%S')
    squawk_rep = {
        'time': pretty_time,
        'username': row[2],
        'text': row[3]
    }
    return squawk_rep


def isValidSquawkForm(form):
    if 'text' not in form:
        return False
    text = form['text']
    if type(text) is str:
        return len(text) <= 140
    else:
        return False


if __name__ == '__main__':
    app.run()
