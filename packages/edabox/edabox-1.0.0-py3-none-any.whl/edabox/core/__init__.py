import pandas as pd
from .io import (
    read_csv,
    read_excel,
    read_frame
)
from .utils import process_frame
from .box import DataBox

# module level doc-string
__doc__ = """
edabox - a library for Python to gain insights into datasets
=====================================================================
**Work in Progress**
-------------
"""

__all__ = [
    "DataBox",
    "read_csv",
    "read_excel",
    "read_frame",
    "process_frame"
]





