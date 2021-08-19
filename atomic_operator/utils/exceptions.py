class IncorrectParameters(Exception):

    """
    Raised when the incorrect configuration of parameters is passed into a Class
    """
    pass


class MissingDefinitionFile(Exception):

    """
    Raised when a definition file cannot be find
    """
    pass


class AtomicsFolderNotFound(Exception):

    """Raised when unable to find a folder containing Atomics
    """
    pass
