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


@app.route('/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/page/<int:page>', methods=['GET', 'POST'])
def root(page):
    err = ""
    status = 200
    if request.form:
        msg = request.form['squawk_msg']
        if len(msg) > 140:
            err = "Invalid Squawk!"
            status = 400
        elif len(msg) > 0:
            query = "INSERT INTO squawks (\'msg\') VALUES (\'" + msg + "\')"
            query_exec = get_db().execute(query, ())
            get_db().commit()
    query = "SELECT COUNT(*) FROM squawks"
    query_exec = get_db().execute(query, ())
    count = query_exec.fetchone()[0]
    return render_template("home.html", num_squawks=count, page=page, error=err), status


@app.context_processor
def utility_processor():
    def get_squawks(page=1):
        query = "SELECT msg FROM squawks ORDER BY timestamp DESC"
        query_exec = get_db().execute(query, ())
        result = query_exec.fetchall()
        query_exec.close()
        p_start = min(len(result) - 1, (page - 1) * 20)
        p_end = min(len(result) - 1, (page * 20) - 1)
        results_to_show = result[p_start:p_end]
        return results_to_show
    return dict(get_squawks=get_squawks)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
