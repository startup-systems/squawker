from flask import Flask, g, render_template, redirect, url_for,\
    request, jsonify
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


class InvalidUsage(Exception):
    '''http://flask.pocoo.org/docs/0.11/patterns/apierrors/'''
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# set the post length as a configuration variable
MAX_LEN = 3
PAGE_LEN = 20


class Squawk:
    def __init__(self, text, ident, timestamp):
        self.text = text
        self.id = ident
        self.timestamp = timestamp


@app.route('/')
@app.route('/page/<int:page_no>')
def root(page_no=0):
    conn = get_db()
    c = conn.cursor()
    squawks = []

    c.execute('\
    SELECT Count(*)\
    FROM squawks')
    count = c.fetchone()[0]

    t = (page_no*PAGE_LEN, PAGE_LEN)

    c.execute('\
    SELECT id, squawk, timestamp\
    FROM squawks\
    ORDER BY timestamp desc\
    LIMIT ?,?', t)
    for squawk in c.fetchall():
        squawks.append(Squawk(squawk[1], squawk[0], squawk[2]))

    return render_template("base.html", squawks=squawks, max_len=MAX_LEN,
                        has_next=(count > ((page_no+1)*PAGE_LEN)),
                        page=page_no)


def isValid(squawk):
    return (len(squawk) <= MAX_LEN) and len(squawk) > 0


@app.route('/post', methods=['POST'])
def post():
    squawk = request.form['squawk']

    if(isValid(squawk)):
        conn = get_db()
        c = conn.cursor()
        c.execute('INSERT INTO squawks (squawk) values (?)', (squawk,))
        conn.commit()
        return redirect(url_for('root'))
    else:
        raise InvalidUsage('Squawk is invalid.', status_code=400)


if __name__ == '__main__':
    app.run()
