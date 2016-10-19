from flask import Flask, g, jsonify, render_template, request, redirect, url_for
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
### Methods ###
#Grab posts
def getPosts(page = 1):
    conn = get_db()
    cur = conn.cursor()
    offset = (page - 1) * 20
    cur.execute("""SELECT id, body FROM
                squawks
                ORDER BY id DESC
                LIMIT 20 OFFSET (?)""", (offset, ))
    temp = cur.fetchall()
    data = []
    idx = []
    #Store values in list
#    for val in temp:
#        data.append(temp[0])
    cur.close()
    return temp

#Add posts
def addPost(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO squawks (body) VALUES(?)", (data,))
    conn.commit()

#### Routes  ######
#Index
@app.route('/')
def root():
    return page(1)
#Pages
@app.route('/<int:pageNum>')
def page(pageNum):
    currPage = pageNum
    squawks = getPosts(pageNum)
    if( squawks[len(squawks) - 1][0] == 1):
      last = True
    else:
      last = False
    # TODO change this
    return render_template('index.html', text=squawks[0], squawks=squawks, currPage=currPage, last=last)
#Add
@app.route('/add/', methods=['POST'])
def add(text=""):
    addPost(request.form["new_body"])
    return redirect(url_for('root'))

#Next
@app.route('/next/', methods=['GET'])
def nextPage():
  pageNum = int(request.path[1:])
  return redirect(url_for('page'), pageNum=pageNum)


if __name__ == '__main__':
    app.run()

# Sources:
# http://stackoverflow.com/questions/109232/what-is-the-best-way-to-paginate-results-in-sql-server
