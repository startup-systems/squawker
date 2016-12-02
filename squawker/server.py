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


@app.route('/', methods=['GET', 'POST'], defaults={'pageN': 1})
@app.route('/page/<int:pageN>', methods=['GET', 'POST'])
def root(pageN):
    status = 200
    if request.form:
        msg = request.form['squawk_msg']
        if len(msg) > 140:
            err = "Msg too long"
            status = 400
        elif len(msg) > 0 and len(msg) <= 140:
            query = "INSERT INTO squawkstable (\'message\') VALUES (\'" + msg + "\')"
            query_exec = get_db().execute(query, ())
            get_db().commit()
            query_exec.close()
    cmd = "SELECT COUNT(*) FROM squawkstable"
    cmdExec = get_db().execute(cmd, ())
    count = cmdExec.fetchone()[0]
    cmdExec.close()
    return render_template("index.html", num_squawks=count, pageN=pageN), status


@app.context_processor
def utility_processor():
    def loadSquawks(pageN=1):
        cmd = "SELECT message FROM squawkstable ORDER BY timestamp DESC"
        cmdExec = get_db().execute(cmd, ())
        squawks = cmdExec.fetchall()
        cmdExec.close()
        slen = len(squawks)
        return squawks[(pageN - 1) * 20:min(slen, pageN * 20)]
    return dict(loadSquawks=loadSquawks)


if __name__ == '__main__':
    app.run()
