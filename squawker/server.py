from flask import Flask, g, request, render_template
import sqlite3


# -- leave these lines intact --
app = Flask(__name__)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker/squawker.db')
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


@app.route('/', methods=['GET', 'POST'], defaults={'pageN': 1})
@app.route('/page/<int:pageN>', methods=['GET', 'POST'])
def root(pageN):
    status = 200
    if request.form:
        msg = request.form['new_squawk']
        if len(msg) > 140:
            err = "Maximum 140 characters"
            status = 400
        elif len(msg) > 0 and len(msg) <= 140:
            query=get_db().execute("INSERT INTO squawktable (\'squawk\') VALUES (\'" + msg + "\')", ())
            get_db().commit()
            query.close()
    command = get_db().execute("SELECT COUNT(*) FROM squawktable", ())
    count = command.fetchone()[0]
    command.close()
    return render_template("index.html", num=count, pageN=pageN), status


@app.context_processor
def utility_processor():
    def loadSquawks(pageN=1):
        command = get_db().execute("SELECT squawk FROM squawktable ORDER BY timestamp DESC", ())
        squawks = command.fetchall()
        command.close()
        return squawks[(pageN - 1) * 20:min(len(squawks), pageN * 20)]
    return dict(loadSquawks=loadSquawks)

if __name__ == '__main__':
    app.run()
