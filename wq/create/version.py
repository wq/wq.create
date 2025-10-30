from importlib.metadata import version, PackageNotFoundError


try:
    VERSION = version("wq.build")
except PackageNotFoundError:
    VERSION = "0.0.0"
