from functools import wraps

# Decorator logging executed actions
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Running action: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper