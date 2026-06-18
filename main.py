from movie_manager import MovieManager
from exceptions import InvalidRatingError, InvalidRegexError, MovieNotFoundError

# Displays application menu
def show_menu():
    print("\n=== Movie Tracker ===")
    print("1. Add movie")
    print("2. Show all movies")
    print("3. Mark movie as watched")
    print("4. Mark movie as unwatched")
    print("5. Rate movie")
    print("6. Search movie by title")
    print("7. Filter movies by genre")
    print("8. Pick a random movie to watch")
    print("9. Show statistics")
    print("10. Show movies sorted by rating")
    print("11. Delete movie")
    print("12. Save data")
    print("13. Exit")

# Validates integer input
def get_int_input(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Error: please enter a number.")

# Validates year input (must contain 4 digits)
def get_year_input(message):
    while True:
        year = input(message).strip()

        if year.isdigit() and len(year) == 4:
            return int(year)

        print("Error: year must contain exactly 4 digits.")

def print_movies(movies):
    movies = list(movies)

    if not movies:
        print("No movies to display.")
        return

    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie}")

# Main application loop
def main():
    manager = MovieManager()

    while True:
        show_menu()
        choice = input("Choose an option: ")

        try:
            if choice == "1":
                title = input("Enter movie title: ")
                year = get_year_input("Enter release year: ")
                genre_input = input("Enter genre(s), separated by commas: ")
                genres = [
                    genre.strip().strip('"').strip("'").lower()
                    for genre in genre_input.split(",")
                    if genre.strip()
                ]
                manager.add_movie(title, year, genres)
                print("Movie has been added.")

            elif choice == "2":
                manager.show_all_movies()

            elif choice == "3":
                title = input("Enter movie title: ")
                movie = manager.find_movie_by_title(title)
                if movie:
                    movie.mark_as_watched()
                else:
                    print("Operation cancelled.")

            elif choice == "4":
                title = input("Enter movie title: ")
                movie = manager.find_movie_by_title(title)
                if movie:
                    movie.mark_as_unwatched()
                else:
                    print("Operation cancelled.")

            elif choice == "5":
                title = input("Enter movie title: ")
                movie = manager.find_movie_by_title(title)
                if movie:
                    attempts = 3
                    while attempts > 0:
                        try:
                            rating = float(input("Enter rating from 0 to 10: "))
                            movie.set_rating(rating)
                            print("Rating has been saved.")
                            break

                        except InvalidRatingError as e:
                            attempts -= 1
                            print(f"Error: {e}")
                            if attempts > 0:
                                print(f"Attempts remaining: {attempts}")
                            else:
                                print("Too many invalid attempts. Returning to menu.")

                        except ValueError:
                            attempts -= 1
                            print("Error: please enter a valid number.")
                            if attempts > 0:
                                print(f"Attempts remaining: {attempts}")
                            else:
                                print("Too many invalid attempts. Returning to menu.")

                else:
                    print("Operation cancelled.")

            elif choice == "6":
                pattern = input("Enter title or part of title: ")
                results = manager.search_by_regex(pattern)
                print_movies(results)

            elif choice == "7":
                genre = input("Enter genre or genres, separated by commas: ")
                results = manager.filter_by_genre(genre)
                print_movies(results)

            elif choice == "8":
                movie = manager.draw_random_unwatched_movie()
                print(f"Suggested movie: {movie}")

            elif choice == "9":
                stats = manager.get_statistics()

                print("\n=== Statistics ===")
                print(f"Total movies: {stats['total']}")
                print(f"Watched movies: {stats['watched']}")
                print(f"Unwatched movies: {stats['unwatched']}")
                print(f"Average rating: {stats['average_rating']}")
                print(f"Highest rated movie(s): {', '.join(stats['highest_rated'])}")

            elif choice == "10":
                sorted_movies = manager.get_movies_sorted_by_rating()
                print_movies(sorted_movies)

            elif choice == "11":
                title = input("Enter movie title to delete: ")
                deleted = manager.delete_movie(title)
                if deleted:
                    print("Movie has been deleted.")
                else:
                    print("Operation cancelled.")

            elif choice == "12":
                manager.save_movies()
                print("Data has been saved.")

            elif choice == "13":
                while True:
                    save_choice = input(
                        "Do you want to save changes before exiting? (1 - Yes, 0 - No): "
                    )
                    if save_choice == "1":
                        manager.save_movies()
                        print("Data saved. Exiting program.")
                        break

                    elif save_choice == "0":
                        print("Exiting program without saving.")
                        break

                    else:
                        print("Invalid choice. Enter 1 or 0.")
                break

            else:
                print("Invalid option. Choose a number from the menu.")

        except InvalidRatingError as error:
            print(f"Rating error: {error}")

        except InvalidRegexError as error:
            print(f"Regex error: {error}")

        except MovieNotFoundError as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()