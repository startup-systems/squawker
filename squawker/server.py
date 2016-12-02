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


@app.context_processor
def utility_processor():
    def loadSquawks(page_number=1):
        query_exec = get_db().execute("SELECT squawk from mysquawktable ORDER BY id DESC", ())
        squawks = query_exec.fetchall()
        query_exec.close()
        squawk_length = len(squawks)
        return squawks[(page_number - 1) * 20:min(squawk_length, page_number * 20)]
    return dict(loadSquawks=loadSquawks)


@app.route('/', methods=['GET', 'POST'], defaults={'page_number': 1})
@app.route('/page/<int:page_number>', methods=['GET', 'POST'])
def root(page_number):
    status = 200
    if request.form:
        message = request.form['squawk_message']
        if len(message) > 140:
            err = "Squawk is too long"
            status = 400
        elif len(message) > 0 and len(message) <= 140:
            query_exec = get_db().execute("INSERT INTO mysquawktable (\'squawk\') VALUES (\'" + message + "\')", ())
            get_db().commit()
            query_exec.close()
    cmd_exec = get_db().execute("SELECT COUNT(*) FROM mysquawktable", ())
    count = cmd_exec.fetchone()[0]
    cmd_exec.close()
    return render_template("index.html", num_squawks=count, page_number=page_number), status


if __name__ == '__main__':
    app.run()
