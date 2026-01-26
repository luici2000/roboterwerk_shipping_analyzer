# Roboterwerk Shipping Analyzer

Ein Python-Tool zur Analyse von Lieferschein-PDFs der Roboterwerk GmbH.

## Features

- **PDF-Extraktion**: Automatische Erkennung aller Lieferscheindaten aus PDF-Dateien
- **SKU-Erkennung**: Unterstützt alle Artikel-Prefixe (RW_, UAV_, UAS_, X-RW-)
- **Deutsche Formatierung**: Zahlen mit Komma (1.234,56 EUR)
- **Multi-Format Export**: CSV (Semikolon-getrennt) und Excel (XLSX)
- **Umfangreiche Analysen**: 8 Excel-Sheets mit detaillierten Auswertungen

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip

### Installation via pip

```bash
pip install -r requirements.txt
```

### Oder manuell

```bash
pip install pymupdf openpyxl
```

## Verwendung

### Kommandozeile

```bash
# Einfache Verwendung
python -m roboterwerk_analyzer lieferscheine.pdf

# Mit Ausgabeverzeichnis
python -m roboterwerk_analyzer lieferscheine.pdf --output ./auswertungen

# Hilfe anzeigen
python -m roboterwerk_analyzer --help
```

### Als Python-Modul

```python
from roboterwerk_analyzer import LieferscheinExtractor, VerkaufsAnalyse, ExportManager

# PDF einlesen
extractor = LieferscheinExtractor("lieferscheine.pdf")
daten = extractor.extrahiere()

# Analyse erstellen
analyse = VerkaufsAnalyse(daten)
analyse.drucke_report()

# Exportieren
exporter = ExportManager(daten, analyse)
exporter.export_csv("daten.csv")
exporter.export_excel("analyse.xlsx")
```

### Deutsche Zahlenformatierung

```python
from roboterwerk_analyzer import DeutscheFormatierung

fmt = DeutscheFormatierung()
print(fmt.euro(1234.56))      # "1.234,56 EUR"
print(fmt.prozent(0.156))     # "15,6 %"
print(fmt.zahl(9876.54, 2))   # "9.876,54"
```

## Ausgabe-Dateien

### CSV-Datei

- Semikolon als Trennzeichen (Excel-kompatibel für DE)
- Deutsche Zahlenformatierung
- UTF-8 Encoding

Beispiel:
```csv
Lieferschein_Nr;Datum;Kunde_Nr;Betrag_EUR;Artikel_Nr;...
186322;26.01.2026;81424;6,42;RW_Light_20x8_single;...
```

### Excel-Datei (8 Sheets)

| Sheet | Inhalt |
|-------|--------|
| Rohdaten | Alle extrahierten Datensätze |
| Zusammenfassung | Kennzahlen (Umsatz, Durchschnitt, Min/Max) |
| Produkt-Analyse | Auswertung nach Produkt-Typ |
| Artikel-Details | Alle Artikelnummern mit Stückzahlen |
| Tages-Analyse | Umsatz pro Tag |
| Farben-Analyse | Farbverteilung |
| Länder-Analyse | Geografische Verteilung |
| Kunden-Analyse | Top Kunden nach Umsatz |

## Unterstützte Artikel-Prefixe

| Prefix | Beschreibung |
|--------|--------------|
| `RW_` | Roboterwerk Standardprodukte |
| `UAV_` | UAV-ID Drohnen-Kennzeichen |
| `UAS_` | UAS Registrierungsbestätigung |
| `X-RW-` | Spezial-Kennzeichen (QR etc.) |

## Projektstruktur

```
roboterwerk_shipping_analyzer/
├── README.md
├── requirements.txt
├── setup.py
├── LICENSE
├── .gitignore
├── roboterwerk_analyzer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── extractor.py
│   ├── analyzer.py
│   ├── exporter.py
│   └── formatting.py
└── examples/
    └── beispiel_verwendung.py
```

## Lizenz

MIT License - siehe [LICENSE](LICENSE)

## Autor

Erstellt für Roboterwerk GmbH
