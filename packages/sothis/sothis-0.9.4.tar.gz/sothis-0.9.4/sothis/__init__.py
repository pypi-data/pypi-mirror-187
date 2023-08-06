from . import fs
from . import helpers
from . import io
from . import nums
from . import search
from .structures import *

__version__ = "0.9.4"

# constants
phi = 1.618033988749895


def randcolor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
