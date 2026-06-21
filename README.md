# MovieTracker

MovieTracker is a simple console application written in Python.

The application allows the user to manage a personal movie list.
The user can add movies, mark them as watched or unwatched, rate them, search by title, filter by genre, get a movie suggestion and display basic statistics.

## Features

* Add new movies
* Show all movies
* Mark movies as watched
* Mark movies as unwatched
* Delete movies
* Rate movies from 0 to 10
* Search movies by title using regular expressions
* Search using full or partial movie titles
* Smart title suggestions for similar matches
* Filter movies by one or multiple genres
* Smart genre suggestions
* Pick a random movie from unwatched movies
* Show movie statistics
* Show movies sorted by rating
* Save and load movie data from a JSON file
* Confirmation before exiting without saving

## Project structure

    movie_tracker/
    |
    ├── main.py
    ├── movie.py
    ├── movie_manager.py
    ├── exceptions.py
    ├── decorators.py
    ├── README.md
    |
    └── data/
        └── movies.json

## How to run

Open the terminal in the main project folder and run:

    cd movie_tracker
    python main.py

If you use PyCharm, open the project and run the main.py file located inside the movie_tracker folder.

## Data storage

Movie data is stored in:

    data/movies.json

The application uses JSON serialization to save and load movie data.

## Example data

The JSON file may contain example movies such as:

    [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": [
            "crime fiction"
        ],
        "rating": 10.0,
        "watched": true
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": [
            "sci-fi"
        ],
        "rating": 9.0,
        "watched": true
    },
    {
        "title": "Dune",
        "year": 2021,
        "genre": [
            "sci-fi"
        ],
        "rating": null,
        "watched": false
    }
    ]

## Menu options

After running the program, the user can choose one of the following options:

1. Add movie
2. Show all movies
3. Mark movie as watched
4. Mark movie as unwatched
5. Rate movie
6. Search movie by title
7. Filter movies by genre
8. Pick a random movie to watch
9. Show statistics
10. Show movies sorted by rating
11. Delete movie
12. Save data
13. Exit

## Input validation

The application validates user input:

* Movie year must contain exactly 4 digits
* Movie rating must be between 0 and 10
* Movie titles can be entered with quotation marks ("" or '')
* Partial movie titles are supported
* Partial genre names are supported
* Invalid regular expressions are handled with an error message

## Used Python elements

The project uses the following Python elements:

* classes and objects
* inheritance
* custom exceptions with inheritance
* custom exception constructors (`__init__`)
* functions
* lambda expressions
* custom decorator
* conditional statements (`if`)
* loops (`for`, `while`)
* comparison and logical operators
* lists
* dictionaries
* sets
* list comprehension
* set comprehension
* generator (`yield`)
* file handling with `with` statement
* JSON serialization and deserialization
* regular expressions (regex)
* error handling with `try / except`
* console user interface (CLI)

## Custom exceptions

The project defines a base custom exception and several specialized exceptions:

- **MovieTrackerError** – base exception for all application-specific errors
- **InvalidRatingError** – raised when a movie rating is outside the allowed range
- **MovieNotFoundError** – raised when a movie cannot be found
- **InvalidRegexError** – raised when an invalid regular expression is provided

Some custom exceptions implement their own constructors (`__init__`) to store additional information about the error and generate detailed error messages.
## Author

Julia Wojciechowska
