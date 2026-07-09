# defusedxml
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See https://www.python.org/psf/license for licensing details.
"""Defuse XML bomb denial of service vulnerabilities
"""
from __future__ import print_function, absolute_import

from .common import (
    DefusedXmlException,
    DTDForbidden,
    EntitiesForbidden,
    ExternalReferenceForbidden,
    NotSupportedError,
    _apply_defusing,
)

def defuse_stdlib():
    """Monkey patch and defuse all stdlib packages

    :warning: The monkey patch is an EXPERIMENTAL feature.
    """
    defused = {}

    from . import ElementTree # nosec
    from . import expatbuilder # nosec
    from . import expatreader  # nosec

    defused_mods = [
        ElementTree,
        expatbuilder,
        expatreader,
    ]

    for defused_mod in defused_mods:
        stdlib_mod = _apply_defusing(defused_mod)
        defused[defused_mod] = stdlib_mod

    return defused


__version__ = "0.8.0rc2"

__all__ = [
    "DefusedXmlException",
    "DTDForbidden",
    "EntitiesForbidden",
    "ExternalReferenceForbidden",
    "NotSupportedError",
]
