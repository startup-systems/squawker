from flask import Flask, g, render_template, request, url_for, abort, redirect
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


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def root(page):
    conn = get_db()
    c = conn.execute('select count(*) from mymessage;')
    count = c.fetchone()[0]
    allthepostmessage = conn.execute('select * from mymessage where id>=(?)-20*(?)+1 and id<=(?)-20*((?)-1) order by id desc;', (count, page, count, page))
    prevpage, nextpage = True, True
    if page == 1:
        prevpage = False
    showout = allthepostmessage.fetchall()
    if len(showout) == 0:
        nextpage = False
    return render_template('index.html', allthepost=enumerate(showout), nowpage=page, prev=prevpage, nextp=nextpage)


@app.route('/submit', methods=['POST', 'GET'])
def formsubmit():
    if len(request.form['msg']) > 140:
        abort(400)
    conn = get_db()
    conn.execute('insert into mymessage (message) values (?);', (request.form['msg'],))
    conn.commit()
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run()
