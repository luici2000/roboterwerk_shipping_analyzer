#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beispiel für die Verwendung des Roboterwerk Shipping Analyzers.

Dieses Skript zeigt, wie man das Modul programmatisch verwenden kann.
"""

import sys
from pathlib import Path

# Füge das übergeordnete Verzeichnis zum Pfad hinzu (für lokale Entwicklung)
sys.path.insert(0, str(Path(__file__).parent.parent))

from roboterwerk_analyzer import (
    LieferscheinExtractor,
    VerkaufsAnalyse,
    ExportManager,
    DeutscheFormatierung
)


def beispiel_formatierung():
    """Zeigt die deutsche Zahlenformatierung."""
    print("=== Deutsche Formatierung ===\n")

    fmt = DeutscheFormatierung()

    # Zahlen formatieren
    print(f"Zahl:    {fmt.zahl(1234.567, 2)}")      # 1.234,57
    print(f"Euro:    {fmt.euro(9876.54)}")          # 9.876,54 EUR
    print(f"Prozent: {fmt.prozent(0.1567)}")        # 15,7 %

    # Deutsche Zahlen parsen
    wert = fmt.parse_deutsch("1.234,56")
    print(f"Geparst: {wert}")  # 1234.56

    print()


def beispiel_analyse(pdf_pfad):
    """Führt eine komplette Analyse durch."""
    print("=== Lieferschein-Analyse ===\n")

    # 1. PDF einlesen
    print(f"Lese PDF: {pdf_pfad}")
    extractor = LieferscheinExtractor(pdf_pfad)
    daten = extractor.extrahiere()

    print(f"Gefunden: {len(daten)} Lieferscheine\n")

    # 2. Analyse erstellen
    analyse = VerkaufsAnalyse(daten)

    # 3. Zusammenfassung abrufen
    zusammenfassung = analyse.zusammenfassung()
    fmt = DeutscheFormatierung()

    print("Zusammenfassung:")
    print(f"  Bestellungen: {zusammenfassung['Anzahl_Bestellungen']}")
    print(f"  Umsatz:       {fmt.euro(zusammenfassung['Gesamtumsatz'])}")
    print(f"  Durchschnitt: {fmt.euro(zusammenfassung['Durchschnitt'])}")
    print()

    # 4. Einzelne Analysen
    print("Top 5 Artikel:")
    artikel = analyse.nach_artikel()
    for i, (art, stats) in enumerate(
        sorted(artikel.items(), key=lambda x: -x[1]['count'])[:5]
    ):
        print(f"  {i+1}. {art}: {stats['count']} Bestellungen")

    print()

    # 5. Kompletten Report drucken
    print("Kompletter Report:")
    analyse.drucke_report()

    # 6. Exportieren
    exporter = ExportManager(daten, analyse)
    exporter.export_csv("beispiel_export.csv")
    exporter.export_excel("beispiel_export.xlsx")


def main():
    """Hauptfunktion."""
    # Formatierungs-Beispiel (benötigt keine PDF)
    beispiel_formatierung()

    # Analyse-Beispiel (benötigt PDF)
    if len(sys.argv) > 1:
        pdf_pfad = sys.argv[1]
        beispiel_analyse(pdf_pfad)
    else:
        print("Für Analyse-Beispiel: python beispiel_verwendung.py <pdf_datei>")


if __name__ == "__main__":
    main()
