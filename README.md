# Squawker (Django)

In this assignment, you will rebuild [Squawker](https://github.com/startup-systems/squawker) in [Django](https://www.djangoproject.com/).

## Requirements

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
