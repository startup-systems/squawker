from flask import Flask, g
import sqlite3


# -- leave these lines intact --
app = Flask(__name__)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker.db')
        g.sqlite_db = sqlite3.connect(db_name)

    return g.sqlite_db
# ------------------------------


@app.route('/')
def hello():
    db = get_db()
    c = db.cursor()
    # ...
    return "Hello World!"


if __name__ == '__main__':
    app.run()
