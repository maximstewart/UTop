# Python imports

# Lib imports

# Application imports



class SingletonError(Exception):
    pass



class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            raise SingletonError(f"'{cls.__name__}' is a Singleton. Cannot create a new instance...")

        cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
