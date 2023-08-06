#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""LISA Instrument module."""

import importlib_metadata

from .instrument import Instrument
from .hexagon import Hexagon


try:
    metadata = importlib_metadata.metadata('lisainstrument').json
    __version__ = importlib_metadata.version('lisainstrument')
    __author__ = metadata['author']
    __email__ = metadata['author_email']
except importlib_metadata.PackageNotFoundError:
    pass
