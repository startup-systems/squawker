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


@app.route('/', methods=['GET', 'POST'])
def root():
    error = ""
    status = 200
    conn = get_db()
    # if click on the post button
    if(request.method == "POST"):
        # get the text from text area id as post_text
        post_text = request.form['post_text']
        # if longer than 140c, shoot ERROR 400
        if len(post_text) > 140:
            error = "Post too long, limit to 140"
            status = 400
        # insert into the database
        else:
            c = conn.execute("INSERT INTO squawks (\'posts\') VALUES (\'" + post_text + "\')")
            conn.commit()
    c = conn.execute("SELECT COUNT(*) FROM squawks", ())
    count = c.fetchone()[0]
    c.close()
    return render_template("index.html", num_squawks=count), status



@app.context_processor
def utility_processor():
    def loadSquawks():
        conn = get_db()
        # sort by DESC time
        c = conn.execute("SELECT posts FROM squawks ORDER BY timestamp DESC ", ())
        squawks = c.fetchall()
        c.close()
        slen = len(squawks)
        return squawks
    return dict(loadSquawks=loadSquawks)


if __name__ == '__main__':
    app.run()
