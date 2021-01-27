from pkg_resources import get_distribution, DistributionNotFound
try:
    VERSION = get_distribution("wq.create").version
except DistributionNotFound:
    VERSION = "0.0.0"
