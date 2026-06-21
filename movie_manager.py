import json
import random
import re
import os

from movie import Movie
from exceptions import MovieNotFoundError, InvalidRegexError
from decorators import log_action

# Class responsible for managing movies and application logic
class MovieManager:
    def __init__(self, file_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if file_path is None:
            self.file_path = os.path.join(base_dir, "data", "movies.json")
        else:
            self.file_path = file_path

        self.movies = []
        self.load_movies()

    @log_action
    def add_movie(self, title, year, genre):
        title = title.strip().strip('"').strip("'").title()

        if isinstance(genre, list):
            genre = [
                g.strip().strip('"').strip("'").lower()
                for g in genre
                if g.strip()
            ]
        else:
            genre = [
                g.strip().strip('"').strip("'").lower()
                for g in genre.split(",")
                if g.strip()
            ]

        movie = Movie(title, year, genre)
        self.movies.append(movie)

    def show_all_movies(self):
        if not self.movies:
            print("No movies in the database.")
            return

        for index, movie in enumerate(self.movies, start=1):
            print(f"{index}. {movie}")

    # Searches movie by title and suggests similar matches
    def find_movie_by_title(self, title):
        title = title.strip().strip('"').strip("'")

        # Exact match
        for movie in self.movies:
            if movie.title.lower() == title.lower():
                return movie

        # Partial matches
        suggestions = [
            movie for movie in self.movies
            if title.lower() in movie.title.lower()
        ]

        if len(suggestions) == 1:
            suggested_movie = suggestions[0]

            print(f'Did you mean "{suggested_movie.title}"?')
            choice = input("Enter 1 for yes or 0 for no: ")

            if choice == "1":
                return suggested_movie
            return None

        elif len(suggestions) > 1:
            print("\nMultiple movies found. Which one did you mean?")

            for index, movie in enumerate(suggestions, start=1):
                print(f"{index}. {movie.title}")

            print("0 - Cancel operation")

            while True:
                choice = input("Choose a number: ")

                if choice == "0":
                    return None

                if choice.isdigit():
                    choice = int(choice)

                    if 1 <= choice <= len(suggestions):
                        return suggestions[choice - 1]

                print("Invalid choice. Try again.")

        raise MovieNotFoundError(title)

    @log_action
    def mark_movie_as_watched(self, title):
        movie = self.find_movie_by_title(title)

        if movie:
            movie.mark_as_watched()
            return True

        return False

    @log_action
    def mark_movie_as_unwatched(self, title):
        movie = self.find_movie_by_title(title)

        if movie:
            movie.mark_as_unwatched()
            return True

        return False

    @log_action
    def rate_movie(self, title, rating):
        movie = self.find_movie_by_title(title)

        if movie:
            movie.set_rating(rating)
            return True

        return False

    @log_action
    def delete_movie(self, title):
        movie = self.find_movie_by_title(title)

        if movie:
            self.movies.remove(movie)
            return True

        return False

    def search_by_regex(self, pattern):
        pattern = pattern.strip().strip('"').strip("'")

        try:
            return [
                movie for movie in self.movies
                if re.search(pattern, movie.title, re.IGNORECASE)
            ]
        except re.error:
            raise InvalidRegexError(pattern)

    # Filters movies by one or multiple genres
    # Supports partial matching and suggestions
    def filter_by_genre(self, genre_input):

        def get_genres_as_list(movie):
            if isinstance(movie.genre, list):
                return movie.genre
            return [movie.genre]

        genre_parts = [
            genre.strip().strip('"').strip("'").lower()
            for genre in genre_input.split(",")
            if genre.strip()
        ]

        all_genres = sorted({
            genre.lower()
            for movie in self.movies
            for genre in get_genres_as_list(movie)
        })

        def choose_from_available_genres():
            print("Choose one of the following genres:")

            for index, genre_name in enumerate(all_genres, start=1):
                print(f"{index}. {genre_name}")

            print("0 - Cancel operation")

            while True:
                choice = input("Choose a number: ")

                if choice == "0":
                    return None

                if choice.isdigit():
                    choice = int(choice)

                    if 1 <= choice <= len(all_genres):
                        return all_genres[choice - 1]

                print("Invalid choice. Try again.")

        selected_genres = []

        for genre in genre_parts:
            exact_matches = [
                existing_genre for existing_genre in all_genres
                if existing_genre.lower() == genre
            ]

            if exact_matches:
                selected_genres.append(exact_matches[0])
                continue

            partial_matches = [
                existing_genre for existing_genre in all_genres
                if genre in existing_genre.lower()
            ]

            if len(partial_matches) == 1:
                suggested_genre = partial_matches[0]

                print(f'Did you mean "{suggested_genre}"?')
                choice = input("Enter 1 for yes or 0 for no: ")

                if choice == "1":
                    selected_genres.append(suggested_genre)

            elif len(partial_matches) > 1:
                print("\nMultiple genres found. Which one did you mean?")

                for index, genre_name in enumerate(partial_matches, start=1):
                    print(f"{index}. {genre_name}")

                print("0 - Cancel operation")

                while True:
                    choice = input("Choose a number: ")

                    if choice == "0":
                        selected_genre = choose_from_available_genres()

                        if selected_genre:
                            selected_genres.append(selected_genre)

                        break

                    if choice.isdigit():
                        choice = int(choice)

                        if 1 <= choice <= len(partial_matches):
                            selected_genres.append(partial_matches[choice - 1])
                            break

                    print("Invalid choice. Try again.")
            else:
                print(f'No matching genre found for "{genre}".')

                selected_genre = choose_from_available_genres()

                if selected_genre:
                    selected_genres.append(selected_genre)

        if not selected_genres:
            return []

        return [
            movie for movie in self.movies
            if all(
                any(
                    g.strip().lower() == selected_genre.strip().lower()
                    for g in get_genres_as_list(movie)
                )
                for selected_genre in selected_genres
            )
        ]

    def get_movies_sorted_by_rating(self):
        return sorted(
            [movie for movie in self.movies if movie.rating is not None],
            key=lambda movie: movie.rating,
            reverse=True
        )

    # Generator returning unwatched movies
    def get_unwatched_movies(self):
        for movie in self.movies:
            if not movie.watched:
                yield movie

    def draw_random_unwatched_movie(self):
        unwatched_movies = list(self.get_unwatched_movies())

        if not unwatched_movies:
            raise MovieNotFoundError("There are no unwatched movies to suggest.")
        return random.choice(unwatched_movies)

    # Generates movie statistics
    def get_statistics(self):
        total = len(self.movies)
        watched = len([movie for movie in self.movies if movie.watched])
        unwatched = total - watched

        rated_movies = [movie for movie in self.movies if movie.rating is not None]
        average_rating = (
            sum(movie.rating for movie in rated_movies) / len(rated_movies)
            if rated_movies else 0
        )

        if rated_movies:
            highest_rating = max(movie.rating for movie in rated_movies)

            highest_rated = [
                movie.title for movie in rated_movies
                if movie.rating == highest_rating
            ]
        else:
            highest_rated = ["none"]

        return {
            "total": total,
            "watched": watched,
            "unwatched": unwatched,
            "average_rating": round(average_rating, 2),
            "highest_rated": highest_rated
        }

    # Saves movie data to JSON file
    @log_action
    def save_movies(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [movie.to_dict() for movie in self.movies],
                file,
                ensure_ascii=False,
                indent=4
            )

    # Loads movie data from JSON file
    def load_movies(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.movies = [Movie.from_dict(movie_data) for movie_data in data]
        except FileNotFoundError:
            self.movies = []
        except json.JSONDecodeError:
            self.movies = []