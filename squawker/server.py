from flask import Flask, g, jsonify, request, url_for
import datetime
import sqlite3
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


@app.route('/')
def root():
    conn = get_db()
    script = url_for('static', filename='js/squawker.js')
    template = env.get_template('index.html')
    return template.render(squawkerScript=script)


@app.route('/squawk', methods=['POST'])
def createSquawk():
    json = request.get_json()
    create_squawk(json)
    return '', 201


@app.route('/squawks', methods=['GET'])
def getAllSquawks():
    squawkRows = get_all_squawks()
    squawkReps = [marshal_squawk_row(row) for row in squawkRows]
    template = env.get_template('feed.html')
    return template.render(squawks=squawkReps)


def create_squawk(data):
    db = get_db()
    c = db.cursor()
    squawk = (data['time'] / 1000.0, data['username'], data['text'])
    c.execute('INSERT INTO squawks(time, username, text) VALUES (?, ?, ?)', squawk)
    db.commit()


def get_all_squawks():
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM squawks ORDER BY TIME DESC')
    all_rows = c.fetchall()
    return all_rows


def marshal_squawk_row(row):
    time = datetime.datetime.fromtimestamp(int(row[1]))
    pretty_time = time.strftime('%Y-%m-%d %H:%M:%S')
    squawk_rep = {
        'time': pretty_time,
        'username': row[2],
        'text': row[3]
    }
    return squawk_rep


if __name__ == '__main__':
    app.run()
