# Custom exception for invalid movie rating
class InvalidRatingError(Exception):
    """Raised when movie rating is outside the allowed range."""
    pass

# Custom exception for missing movie
class MovieNotFoundError(Exception):
    """Raised when a movie cannot be found."""
    pass

# Custom exception for invalid regex patterns
class InvalidRegexError(Exception):
    """Raised when the regex pattern is invalid."""
    pass