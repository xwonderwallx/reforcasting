class Singleton(object):
    """
    A base class for implementing the Singleton design pattern.

    This class ensures that only one instance of any subclass can exist. Subsequent
    attempts to create an instance of a subclass will return the existing instance.
    This behavior is achieved by overriding the `__new__` method.

    Attributes:
        _instances (dict): A class-level dictionary that stores instances of subclasses.
                           The keys are subclass types, and the values are the corresponding
                           singleton instances.

    Methods:
        __new__(cls, *args, **kwargs): Overrides the default object allocator.
                                       Ensures that only one instance of a subclass is created.
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
        Overrides the default object allocator to implement the Singleton pattern.

        This method checks if an instance of the subclass already exists in the `_instances`
        dictionary. If it does, that instance is returned. If not, a new instance is created,
        stored in `_instances`, and then returned. This ensures that only one instance of
        each subclass can exist.

        Parameters:
            cls: The class for which `__new__` is called.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The singleton instance of the subclass.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]
