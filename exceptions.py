# Base exception for all custom MovieTracker errors
class MovieTrackerError(Exception):
    """Base exception for MovieTracker."""
    pass


# Custom exception for invalid movie rating
class InvalidRatingError(MovieTrackerError):
    """Raised when movie rating is outside the allowed range."""

    def __init__(self, rating):
        self.rating = rating
        super().__init__(f"Rating {rating} is invalid. Rating must be between 0 and 10.")


# Custom exception for missing movie
class MovieNotFoundError(MovieTrackerError):
    """Raised when a movie cannot be found."""

    def __init__(self, title):
        self.title = title
        super().__init__(f'Movie "{title}" was not found.')


# Custom exception for invalid regex pattern
class InvalidRegexError(MovieTrackerError):
    """Raised when the regex pattern is invalid."""

    def __init__(self, pattern):
        self.pattern = pattern
        super().__init__(f'Regex pattern "{pattern}" is invalid.')