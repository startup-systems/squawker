from flask import (Flask, g, render_template,
                   url_for, redirect, request, make_response)
import sqlite3
import time


# -- leave these lines intact --
app = Flask(__name__)

squawks = []


def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker.db')
        g.sqlite_db = sqlite3.connect(db_name)

    return g.sqlite_db


def add_to_db(squawk):
    conn = get_db()
    cur = conn.cursor()
    # create table is does not exist
    conn.execute(
        'CREATE TABLE IF NOT EXISTS mytable (id integer, squawk TEXT)')
    # Execute command
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM mytable")
    numberOfRecords = cur.fetchone()
    cur.execute("INSERT INTO mytable VALUES (?,?)",
                (numberOfRecords[0], squawk))
    conn.commit()

    # Commit changes

    msg = "Record successfully added"

    # close connection
    # conn.close()


def get_from_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("select * from mytable")

    # print all records to database
    # is an array of tuples

    results = cur.fetchall()

    conn.commit()

    # close connection
    # conn.close()

    return results


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


# @app.route('/index')
# def index():


#     # TODO change this

#     #return html form
#     return render_template('index.html',
#         saves = get_from_db())

@app.route('/save', methods=['POST'])
def save():
    # squawks.append(request.form['name'].encode("utf-8"))
    # for squawk in squawks:
    #     print len(squawk)

    result = request.form['name'].encode("utf-8")
    if len(result) <= 140:
        add_to_db(result)
    # Will get new squawk, and save into database
    #  results = get_from_db()
    # print "From Save: num from results: "+str(len(results))
    # for result in results:
    #     print result[1]
    else:

    response = make_response(redirect(url_for('index')))
    return response


@app.route('/')
# IMPORTANT FROM LINK: http://stackoverflow.com/questions/33743658/flask-how-to-update-html-table-with-data-from-sqlite-on-homepage-after-data-are
# The function you defined is mapped to the route you specified, but you can redirect
# from another page to a function, then flask will render the correct route!!!s
def index():
    # conn = init_db() # this may restart the database with no values!
    # TODO change this
    results = get_from_db()
    # print "num from results: " + str(len(results))
    # return html form
    return render_template('index.html',
                           saves=results[::-1])


if __name__ == '__main__':
    app.run(debug=True)
