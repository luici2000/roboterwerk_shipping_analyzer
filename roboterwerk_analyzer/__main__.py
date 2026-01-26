#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kommandozeilen-Interface für den Roboterwerk Shipping Analyzer.

Verwendung:
    python -m roboterwerk_analyzer <pdf_datei>
    python -m roboterwerk_analyzer <pdf_datei> --output <verzeichnis>
    python -m roboterwerk_analyzer --help
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from . import __version__
from .extractor import LieferscheinExtractor
from .analyzer import VerkaufsAnalyse
from .exporter import ExportManager


def parse_args():
    """Parst Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(
        prog='roboterwerk_analyzer',
        description='Analysiert Roboterwerk Lieferschein-PDFs und erstellt Verkaufsreports.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Beispiele:
  python -m roboterwerk_analyzer lieferscheine.pdf
  python -m roboterwerk_analyzer lieferscheine.pdf --output ./reports
  python -m roboterwerk_analyzer lieferscheine.pdf --no-excel
        '''
    )

    parser.add_argument(
        'pdf_datei',
        type=str,
        help='Pfad zur PDF-Datei mit Lieferscheinen'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Ausgabeverzeichnis (Standard: gleiches Verzeichnis wie PDF)'
    )

    parser.add_argument(
        '--no-csv',
        action='store_true',
        help='Keine CSV-Datei erstellen'
    )

    parser.add_argument(
        '--no-excel',
        action='store_true',
        help='Keine Excel-Datei erstellen'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Keine Konsolenausgabe (außer Fehlern)'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser.parse_args()


def main():
    """Hauptfunktion."""
    args = parse_args()

    pdf_pfad = Path(args.pdf_datei)

    # Prüfe ob Datei existiert
    if not pdf_pfad.exists():
        print(f"FEHLER: Datei nicht gefunden: {pdf_pfad}", file=sys.stderr)
        sys.exit(1)

    # Ausgabeverzeichnis
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = pdf_pfad.parent

    # Extrahieren
    if not args.quiet:
        print(f"\nVerarbeite: {pdf_pfad}")

    try:
        extractor = LieferscheinExtractor(pdf_pfad)
        daten = extractor.extrahiere(verbose=not args.quiet)
    except Exception as e:
        print(f"FEHLER beim Extrahieren: {e}", file=sys.stderr)
        sys.exit(1)

    if not daten:
        print("FEHLER: Keine Daten extrahiert.", file=sys.stderr)
        sys.exit(1)

    # Analysieren
    analyse = VerkaufsAnalyse(daten)

    if not args.quiet:
        analyse.drucke_report()

    # Exportieren
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    basis_name = pdf_pfad.stem[:30]  # Kürzen falls zu lang

    exporter = ExportManager(daten, analyse)

    if not args.no_csv:
        csv_pfad = output_dir / f"{basis_name}_daten_{timestamp}.csv"
        exporter.export_csv(csv_pfad)

    if not args.no_excel:
        xlsx_pfad = output_dir / f"{basis_name}_analyse_{timestamp}.xlsx"
        exporter.export_excel(xlsx_pfad)

    if not args.quiet:
        print(f"\nFertig! Dateien gespeichert in: {output_dir}")


if __name__ == "__main__":
    main()
