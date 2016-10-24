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


@app.route('/')
def root():
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT ID, Tweet_Message from squawks order by id desc')
    # iterate over all squawks and store
    squawks_list = cursor_object.fetchall()
    count = len(squawks_list)
    squawks = get_squawks_for_page(squawks_list, page, PER_PAGE)
    if not squawks and page != 1:
        abort(404)
    return render_template('index.html', squawks=squawks)



# add a squawk via post request
@app.route('/add_squawk', methods=['POST'])
def add_squawk():
    if len(request.form['Tweet_Message']) > 140:
        abort(400)
    conn = get_db()
    conn.execute('INSERT INTO squawks (Tweet_Message) VALUES (?)', [request.form['Tweet_Message']])
    conn.commit()
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()