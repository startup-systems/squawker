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

* Pagination
    * The squawks are shown 20 at a time
    * There's a `Next` link to see older squawks, if there are any
