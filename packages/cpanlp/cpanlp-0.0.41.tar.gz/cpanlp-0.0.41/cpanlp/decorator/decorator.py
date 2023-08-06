from functools import wraps
def with_side_effects(sideeffects):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            fn.side_effects = sideeffects
            print("Possible Side Effects:")
            if hasattr(fn, 'side_effects'):
                for effect in fn.side_effects:
                    print(f"- {effect}")
            return result
        return wrapper
    return decorator