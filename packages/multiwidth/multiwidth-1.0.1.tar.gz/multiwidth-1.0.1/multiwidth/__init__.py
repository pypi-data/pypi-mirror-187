"""A Python module for reading/writing fixed-width files with variable column widths"""

from .multiwidth import (
    split,
    get_letter_locations,
    process_line,
    load,
    loads,
    dumps,
    dump,
)

__version__ = "1.0.1"
