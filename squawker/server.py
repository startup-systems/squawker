from flask import Flask, g
import sqlite3
from flask import render_template
from flask import request, session, url_for, redirect, abort, g, flash, _app_ctx_stack


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
# @app.route('/')
# def root():
#     conn = get_db()
#     #TODO change this
#     return "Hello, post a new squawk!"
@app.route('/', methods=["POST", "GET"])
def root():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        new_msg = request.form.get('msg')
        if len(new_msg) > 140:
            return "Length error! Reduce length of squawk to 140 characters or less.", 400
        else:
            query = "INSERT INTO squawker (squawk) VALUES (?)"
            c.execute(query, [new_msg])
            conn.commit()
    selectquery = "SELECT squawk FROM squawker order by id DESC"
    c.execute(selectquery)
    all = c.fetchall()
    c.close()
    return render_template("form.html", squawks=all)
# @app.route('/') #set default?
# @app.route('/', method=["GET","POST"])
#
# def root(page):
#     return render_template('form.html')
# @app.route('/hello')
# def hello():
#     return 'Hello, World'
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % username

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()


# #@app.route('/hello/')
# @app.route('/hello/<name>')

# def hello(name=None):
#     return render_template('hello.html', name=name)


# with app.test_request_context('/hello', method='POST'):
#     # now you can do something with the request until the
#     # end of the with block, such as basic assertions:
#     assert request.path == '/hello'
#     assert request.method == 'POST'


# # To record whatever is submitted via the form.
# @app.route('/add_message', methods=['POST'])
# def add_message():
#     """Registers a new message for the user."""
#     # if 'user_id' not in session:
#     #     abort(401)
#     if request.form['text']:
#         db = get_db()
#         db.execute('''insert into message (text, pub_date) values (?, ?)''', (request.form['text'], int(time.time())))
#         db.commit()
#         flash('Your message was recorded')
#     return redirect(url_for('timeline'))


# # To display everything that has been submitted by the form.
# @app.route('/public')
# def public_timeline():
#     """Displays the latest messages of all users."""
#     return render_template('timeline.html', messages=query_db('''
#         select message.* from message where order by message.pub_date desc limit ?''', [PER_PAGE]))

# #Is this necessary? The previous function effectively does the work.
# @app.route('/')
# def timeline():
#     """Shows a users timeline or if no user is logged in it will
#     redirect to the public timeline.  This timeline shows the user's
#     messages as well as all the messages of followed users.
#     """
#     return render_template('timeline.html', messages=query_db('''select message.* from message
#         where
#         order by message.pub_date desc limit ?''',
#         [PER_PAGE]))

# if __name__ == '__main__':
#     app.run()