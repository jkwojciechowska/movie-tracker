from exceptions import InvalidRatingError

# Class representing a single movie
class Movie:
    def __init__(self, title, year, genre, rating=None, watched=False):
        self.title = title
        self.year = year
        self.genre = genre
        self.rating = rating
        self.watched = watched

    def mark_as_watched(self):
        if self.watched:
            print("Error: Movie has already been watched.")
        else:
            self.watched = True
            print("Movie marked as watched.")

    def mark_as_unwatched(self):
        if not self.watched:
            print("Error: Movie has not been watched yet.")
        else:
            self.watched = False
            print("Movie marked as unwatched.")

    def set_rating(self, rating):
        if rating < 0 or rating > 10:
            raise InvalidRatingError("Rating must be between 0 and 10.")
        self.rating = rating

    # Converts movie object to dictionary for JSON serialization
    def to_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
            "rating": self.rating,
            "watched": self.watched
        }

    # Creates a Movie object from JSON data
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["year"],
            data["genre"],
            data.get("rating"),
            data.get("watched", False)
        )

    # Returns readable movie information
    def __str__(self):
        status = "watched" if self.watched else "unwatched"
        rating = self.rating if self.rating is not None else "no rating"

        if isinstance(self.genre, list):
            genres = ", ".join(self.genre)
        else:
            genres = self.genre

        return f"{self.title} ({self.year}) | {genres} | {status} | rating: {rating}"