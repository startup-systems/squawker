# Squawker

In this assignment, you will build simplified Twitter clone. We'll refer to the individual messages as "squawks".

## Requirements

* The home page (`/`) contains:
    * A single form, to post a new squawk
    * All past squawks, from newest to oldest
* Submitting the form:
    * Creates a new squawk
    * Shows the user the updated homepage (**5%**)
* Squawks are limited to 140 characters
    * Client-side (**5%**)
        * Use HTML5 form validation
    * Server-side (**10%**)
        * The server responds with a status code of 400 if the form is submitted with invalid data.
* The site works without JavaScript
* Built using [Flask](http://flask.pocoo.org/) and SQLite

### Extra credit

* Pagination
    * The squawks are shown 20 at a time
    * There's a `Next` link to see older squawks, if there are any
