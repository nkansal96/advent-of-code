import importlib
import pkgutil


def initialize(package):
    """
    Recursively import all subpackages to initialize the solutions by instantiating the functions
    with the @solution decorators.
    """
    package = importlib.import_module(package)
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        importlib.import_module(full_name)
        if is_pkg:
            initialize(full_name)


initialize(__name__)
