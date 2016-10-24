# Squawker

In this assignment, you will build simplified Twitter clone. We'll refer to the individual messages as "squawks".

## Requirements

* The homepage (`/`) contains:
    * A single form, to post a new squawk (**5%**)
    * All past squawks (**20%**)
        * Sorted from newest to oldest (**20%**)
* Submitting the form:
    1. Creates a new squawk (**30%**)
    1. Shows / takes the user back to the homepage (**5%**)
        * In other words, they should see the updated homepage with the new squawk.
* Squawks are limited to 140 characters
    * Client-side (**5%**)
        * Uses HTML5 form validation
    * Server-side (**10%**)
        * Responds with a status code of 400 if the form is submitted with invalid data.
* Passes Code Climate checks (**5%**)
* The site works without JavaScript
* Built using [Flask](http://flask.pocoo.org/) and [`sqlite3`](https://docs.python.org/3/library/sqlite3.html)

Visual styling is not considered as part of the score, though feel free to get creative! In other words, feel free to make your site pretty, but not a problem if it isn't.

### Extra credit

* Pagination (**20%**)
    * The squawks are shown 20 at a time
    * There's a `Next` link to see older squawks, if there are any

## Setup

1. Update your [VM](https://github.com/startup-systems/vm), if you didn't do so for the [time](https://docs.google.com/document/d/15VzRMLHLGm_l9dzUObQlsOoY12J_jH3U0b9Bu2yi6EI/edit#heading=h.lyptz0o698my) assignment already. From your host machine:

    ```shell
    cd path/to/vm/
    git pull -s recursive -X ours https://github.com/startup-systems/vm.git master
    vagrant reload
    ```

1. [Set up the database.](#set-up-the-database)

## Development workflow

1. Start the server. From your VM:

    ```shell
    cd /vagrant/squawker
    pip3 install -r requirements.txt
    FLASK_APP=squawker/server.py FLASK_DEBUG=1 flask run --host=0.0.0.0
    ```

1. Open http://localhost:5000 from your host machine.
1. Modify [`squawker/server.py`](squawker/server.py).
1. Refresh.

## Set up the database

Note that this will delete any existing content.

1. Modify the [`squawker/schema.sql`](squawker/schema.sql) file.
1. Run

    ```shell
    FLASK_APP=squawker/server.py flask initdb
    ```
Repeat these steps when you need to update the schema.

## Running tests locally

Run the following from this directory:

```shell
# run the pytests
pytest --tb short
# run the pep8 checks
pep8
# check the extra credit
pytest --tb short --runxfail
```

## Things you will need

* [Flask template(s)](http://flask.pocoo.org/docs/0.11/quickstart/#rendering-templates)
    * [Jinja2 syntax](http://jinja.pocoo.org/docs/dev/templates/)
* An [HTML form](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Forms)
* Change/addition of routes in Flask
* Some basic SQL understanding
* SQLite3 CLI
    * Useful for inspecting your database
    * Install in your VM with

        ```shell
        sudo apt-get update
        sudo apt-get install sqlite3
        ```

### Code Climate checks

If you want to try running these locally:

1. [Install Docker](https://docs.docker.com/engine/installation/linux/ubuntulinux/) (follow the "Ubuntu Xenial 16.04 (LTS)" instructions)
1. Run the [Code Climate CLI](https://github.com/codeclimate/codeclimate#readme).

Note that **this is advanced**, so don't worry if you have trouble getting it running.
