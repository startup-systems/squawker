# Squawker (Django)

In this assignment, you will rebuild [Squawker](https://github.com/startup-systems/squawker) in [Django](https://www.djangoproject.com/).

## Requirements

* Passes all of the following on Travis CI:
    * The homepage (`/`) contains:
        * A single form, to post a new squawk (**5%**)
        * All past squawks (**20%**)
            * Sorted from newest to oldest (**10%**)
    * Submitting the form:
        1. Creates a new squawk (**20%**)
        1. Shows / takes the user back to the homepage (**5%**)
            * In other words, they should see the updated homepage with the new squawk.
    * Squawks are limited to 140 characters
        * Client-side (**5%**)
            * Uses HTML5 form validation
        * Server-side (**10%**)
            * Responds with a status code of 400 if the form is submitted with invalid data.
    * Passes Code Climate checks (**5%**)
* Works without JavaScript
* Deployed to Heroku at `<NETID>-squawker.herokuapp.com` (**20%**)

Visual styling is not considered as part of the score, though feel free to get creative! In other words, feel free to make your site pretty, but not a problem if it isn't.

### Extra credit

* Pagination (**10%**)
    * The squawks are shown 20 at a time
    * There's a `Next` link to see older squawks, if there are any

## Setup

1. You will need to set up the project dependencies yourself. Add the following to your [`requirements.txt`](requirements.txt):

    ```
    Django~=1.10.2
    pep8~=1.7.0
    pytest~=3.0.3
    pytest-django~=3.0.0
    pytest-json~=0.4.0
    git+https://github.com/startup-systems/splinter.git@acfac451ee3943e1e155d06249f6ed0aa851b948#egg=splinter[django]
    ```

1. You will set up Django project in your copy of this repository yourself. The easiest way to do this is to run the following from this directory:

    ```sh
    django-admin startproject squawker .
    ```

1. If your project is named something other than `squawker`, you will need to modify the `DJANGO_SETTINGS_MODULE` value in [`pytest.ini`](pytest.ini) to match.
1. Run Django with the following from within your [virtual machine](https://github.com/startup-systems/vm):

    ```sh
    python3 manage.py runserver 0.0.0.0:8000
    ```

### Deploying to Heroku

#### Support PostgreSQL

Django will use SQLite3 as it's database by default, but you'll use PostgreSQL ("Postgres") on Heroku. To make the switch:

1. Install the system-level dependencies.

    ```sh
    sudo apt-get update
    sudo apt-get install libpq-dev
    ```

1. Add the following to your [`requirements.txt`](requirements.txt) file:

    ```
    dj-database-url~=0.4.1
    psycopg2~=2.6.2
    ```

1. Install the Python dependencies.

    ```sh
    pip3 install -r requirements.txt
    ```

1. In your `<project>/settings.py` file:

    ```python
    # add this near the top
    import dj_database_url

    # replace the DATABASES config
    DATABASES = {
        "default": dj_database_url.config(default='sqlite:///db.sqlite3'),
    }
    ```

#### Specify Python version

https://devcenter.heroku.com/articles/python-runtimes

#### Additional setup

1. Create a directory for static files inside the Django project directory.

    ```sh
    mkdir -p <project>/static
    touch <project>/static/.keep
    ```

1. Follow [steps in Heroku documentation](https://devcenter.heroku.com/articles/django-app-configuration#migrating-an-existing-django-project).
    * Skip the database connection parts, since we covered those already.
1. Commit all changes.

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

### Code Climate checks

To run locally, see [the instructions](https://docs.google.com/document/d/1-hk6GzhV1yHU1T0E7uqcdNTtvv3fuq1_WECQOWOT2zw/edit#heading=h.w5f2vmvyb0n).
