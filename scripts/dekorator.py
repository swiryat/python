def uppercase_decorator(func):
    def wrapper(text):
        return func(text).upper()
    return wrapper

@uppercase_decorator
def greet(name):
    return f"Привет, {name}"

print(greet("Алиса"))  # "ПРИВЕТ, АЛИСА"
