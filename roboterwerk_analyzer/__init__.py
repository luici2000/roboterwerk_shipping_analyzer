# -*- coding: utf-8 -*-
"""
Roboterwerk Shipping Analyzer
=============================

Ein Tool zur Analyse von Lieferschein-PDFs der Roboterwerk GmbH.

Beispiel:
    >>> from roboterwerk_analyzer import LieferscheinExtractor, VerkaufsAnalyse
    >>> extractor = LieferscheinExtractor("lieferscheine.pdf")
    >>> daten = extractor.extrahiere()
    >>> analyse = VerkaufsAnalyse(daten)
    >>> analyse.drucke_report()
"""

__version__ = '1.0.0'
__author__ = 'Roboterwerk GmbH'

from .formatting import DeutscheFormatierung
from .extractor import LieferscheinExtractor
from .analyzer import VerkaufsAnalyse
from .exporter import ExportManager

__all__ = [
    'DeutscheFormatierung',
    'LieferscheinExtractor',
    'VerkaufsAnalyse',
    'ExportManager',
]
