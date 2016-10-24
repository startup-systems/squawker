from flask import Flask, g, request, render_template
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

@app.route('/', methods=["GET", "POST"])
def root():
    conn = get_db()
    c = conn.cursor()
    status = 200
    if request.method == "POST":
        message = request.form['squawk']
        if len(message) > 140:
            status = 400
        elif len(message) > 0:
            c.execute("INSERT INTO squawks (squawk) VALUES (\'" + message + "\')")
            conn.commit()
    squawks = c.execute("SELECT squawk FROM squawks ORDER BY timestamp DESC")
    squawks_msgs = squawks.fetchall()
    conn.close()
    return render_template('index.html', squawks=squawks_msgs), status

if __name__ == '__main__':
    app.run(host="0.0.0.0")
