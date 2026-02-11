# CLAUDE.md - Projektanweisungen für Claude Code

## Projekt-Übersicht

**Roboterwerk Shipping Analyzer** ist ein Python-Paket (v1.0.0) zur Analyse von Lieferschein-PDFs der Roboterwerk GmbH. Das Tool extrahiert strukturierte Daten aus PDF-Dateien, erstellt Verkaufsanalysen und exportiert Ergebnisse in CSV- und Excel-Formate mit deutscher Lokalisierung.

**Firma:** Roboterwerk GmbH (Drohnen-Zubehör und Kennzeichen)
**Sprache:** Gesamtes Projekt ist auf Deutsch (Variablennamen, Kommentare, UI-Texte, Dokumentation)

---

## Schnellstart

### Installation

```bash
pip install -r requirements.txt
```

Abhängigkeiten:
- `PyMuPDF>=1.23.0` (PDF-Verarbeitung, importiert als `fitz`)
- `openpyxl>=3.1.0` (Excel-Export)

### Ausführung

```bash
# CLI
python -m roboterwerk_analyzer <pdf_datei>
python -m roboterwerk_analyzer <pdf_datei> --output ./auswertungen
python -m roboterwerk_analyzer <pdf_datei> --no-excel --quiet

# Als Modul
from roboterwerk_analyzer import LieferscheinExtractor, VerkaufsAnalyse, ExportManager, DeutscheFormatierung
```

---

## Architektur und Module

```
roboterwerk_analyzer/
├── __init__.py        # Package-Exports: LieferscheinExtractor, VerkaufsAnalyse, ExportManager, DeutscheFormatierung
├── __main__.py        # CLI-Einstiegspunkt mit argparse (Funktion: main())
├── extractor.py       # Klasse LieferscheinExtractor - PDF-Datenextraktion
├── analyzer.py        # Klasse VerkaufsAnalyse - Statistische Auswertungen
├── exporter.py        # Klasse ExportManager - CSV/Excel-Export
└── formatting.py      # Klasse DeutscheFormatierung - Zahlen-/Währungsformatierung
```

### Datenfluss

```
PDF-Datei
  → LieferscheinExtractor.extrahiere()     → list[dict] (Rohdaten)
    → VerkaufsAnalyse(daten)               → Analyse-Objekt
      → ExportManager(daten, analyse)
        → .export_csv(pfad)                → CSV-Datei (Semikolon-getrennt, UTF-8)
        → .export_excel(pfad)              → XLSX-Datei (8 Sheets)
```

### Zentrale Datenstruktur

Jeder Lieferschein wird als Dictionary dargestellt:

```python
{
    'Seite': int,                # PDF-Seitennummer
    'Lieferschein_Nr': str,      # z.B. "186322"
    'Datum': str,                # Format: "DD.MM.YYYY"
    'Kunde_Nr': str,             # z.B. "81424"
    'Amazon_Bestellung': str,    # Bestellnummer
    'Bestelldatum': str,         # Format: "DD.MM.YYYY"
    'Betrag': float,             # Betrag in EUR als float
    'Artikel_Nr': str,           # z.B. "RW_Light_20x8_single"
    'Produkt_Typ': str,          # Einer von: Drohnen-Plakette, Führerschein, Registrierungsbestätigung, Zubehör, Sonstig
    'Farbe': str,                # z.B. Silber, Schwarz, Gold, Weiß, Rot, Blau, Naturfarben, Grau
    'Menge': int,                # Stückzahl (Standard: 1)
    'Land_Code': str,            # ISO-3 Code z.B. "DEU"
    'Land': str,                 # Vollname z.B. "Deutschland"
}
```

---

## Modul-Details

### extractor.py - LieferscheinExtractor

- Verwendet **PyMuPDF** (`fitz`) zum Lesen von PDF-Seiten
- Regex-basierte Extraktion pro Seite (`_extrahiere_seite()`)
- Erkennt Artikel-Prefixe: `RW_`, `UAV_`, `UAS_`, `X-RW-` (Konstante `ARTIKEL_PREFIXE`)
- Enthält Ländercode-Mapping für 23 europäische Länder (Konstante `LAENDER`)
- Beträge werden aus Debug-Tags extrahiert: `[DBG amount=X,XX EUR]`
- Farberkennung dual: aus Freitext und aus Artikelnummer-Suffixen (`_BL`, `_RO`, `_BLAU`, `_NA`, `_GR`)
- Land wird aus E-ID-Patterns extrahiert (z.B. `DEUxxxxxxxx`)

### analyzer.py - VerkaufsAnalyse

Stellt 7 Analysemethoden bereit:
- `zusammenfassung()` → Kennzahlen (Anzahl, Umsatz, Durchschnitt, Min, Max, Median, Stück)
- `nach_produkt_typ()` → Gruppierung nach Produkttyp
- `nach_artikel()` → Gruppierung nach Artikelnummer
- `nach_tag()` → Gruppierung nach Versanddatum
- `nach_farbe()` → Gruppierung nach Farbe
- `nach_land()` → Gruppierung nach Land
- `nach_kunde()` → Gruppierung nach Kundennummer
- `drucke_report()` → Formatierte Konsolenausgabe

Alle Gruppierungsmethoden nutzen `collections.defaultdict` und geben Dictionaries mit `count`, `umsatz` (und teils `stueck`, `artikel`) zurück.

### exporter.py - ExportManager

- **CSV-Export:** Semikolon als Delimiter, deutsche Zahlenformatierung, UTF-8
- **Excel-Export:** 8 Sheets mit openpyxl-Styling:
  1. Rohdaten
  2. Zusammenfassung (Kennzahlen)
  3. Produkt-Analyse
  4. Artikel-Details
  5. Tages-Analyse
  6. Farben-Analyse
  7. Länder-Analyse
  8. Kunden-Analyse (Top 20 nach Umsatz, einmalige vs. Mehrfach-Käufer)
- Excel-Formate: `#.##0,00 €` für Euro, `0,0%` für Prozent
- Automatische Spaltenbreite (`auto_width`)
- Gestylte Header (weiß auf blau: `#4472C4`)

### formatting.py - DeutscheFormatierung

- `zahl(wert, dezimalstellen)` → `"1.234,56"` (Punkt als Tausendertrennzeichen, Komma als Dezimaltrenner)
- `euro(wert)` → `"1.234,56 EUR"`
- `prozent(wert)` → `"15,6 %"` (Eingabe als Dezimalzahl 0.0-1.0)
- `parse_deutsch(text)` → float (parst deutsche Zahlen zurück)
- Versucht `de_DE.UTF-8` Locale zu setzen, fällt auf manuelle Formatierung zurück

---

## Konventionen und Stil

### Sprache
- **Alle** Bezeichner (Klassen, Methoden, Variablen, Parameter) sind auf Deutsch
- Docstrings auf Deutsch
- CLI-Ausgaben und Fehlermeldungen auf Deutsch
- Ausnahme: Standard-Python-Begriffe wie `self`, `args`, `return`, Bibliotheks-Imports

### Namenskonventionen
- Klassen: PascalCase auf Deutsch (z.B. `VerkaufsAnalyse`, `DeutscheFormatierung`)
- Methoden/Funktionen: snake_case auf Deutsch (z.B. `extrahiere()`, `drucke_report()`, `nach_produkt_typ()`)
- Private Methoden: mit Unterstrich-Prefix (z.B. `_extrahiere_seite()`, `_bestimme_produkt_typ()`)
- Konstanten: UPPER_SNAKE_CASE (z.B. `ARTIKEL_PREFIXE`, `LAENDER`)
- Variablen: snake_case auf Deutsch (z.B. `betraege`, `daten_liste`, `pfad`)

### Code-Stil
- UTF-8 Encoding-Header in jeder Datei: `# -*- coding: utf-8 -*-`
- Python 3.8+ kompatibel (kein Walrus-Operator in kritischen Pfaden, keine `|`-Union-Types)
- f-Strings für Formatierung
- `pathlib.Path` statt `os.path`
- Type Hints werden aktuell NICHT verwendet
- Keine externen Test-Frameworks eingerichtet

### Fehlerbehandlung
- ImportError mit hilfreicher Installationsanweisung bei fehlenden Dependencies
- FileNotFoundError bei fehlenden PDFs
- Graceful Fallback bei Locale-Problemen
- CLI gibt `sys.exit(1)` bei Fehlern zurück

---

## Wichtige Patterns

### Regex-Patterns in extractor.py
- Lieferschein-Nr: `r'Lieferschein\s+(\d+)'`
- Datum: `r'Datum\s*\n?\s*(\d{2}\.\d{2}\.\d{4})'`
- Betrag: `r'\[DBG amount=([\d,]+)\s*EUR\]'` (aus Debug-Tags)
- Amazon-Bestellung: `r'Bestellung Nr\.\s+([\d-]+)\s+vom\s+(\d{2}\.\d{2}\.\d{4})'`
- Menge: `r'(\d)\s*Kennzeichen'`
- Artikel-Nr: `r'\n({prefix}[\w_-]+)'` (dynamisch pro Prefix)
- E-ID/Land: Mehrstufige Regex-Kaskade mit Fallbacks

### Produkt-Typ-Erkennung (Keyword-basiert)
- "führerschein" / "kompetenznachweis" → Führerschein
- "registrierungsbestätigung" → Registrierungsbestätigung
- "kennzeichen" / "plakette" / "uav-id" → Drohnen-Plakette
- "kartenschuber" / "schutzhülle" / "hülle" → Zubehör
- Fallback → Sonstig

---

## Entwicklungshinweise

### Neue Artikel-Prefixe hinzufügen
→ `extractor.py`, Konstante `ARTIKEL_PREFIXE` erweitern

### Neue Länder hinzufügen
→ `extractor.py`, Konstante `LAENDER` erweitern (ISO-3 Code → deutscher Name)

### Neue Farben hinzufügen
→ `extractor.py`, Methode `_extrahiere_farbe()`: Liste `farben` und/oder Artikelnummer-Suffixe erweitern

### Neuen Produkt-Typ hinzufügen
→ `extractor.py`, Methode `_bestimme_produkt_typ()`: Keyword-Bedingung ergänzen

### Neues Excel-Sheet hinzufügen
→ `exporter.py`, Methode `export_excel()`: Neuen Sheet-Block nach dem Pattern der bestehenden Sheets einfügen (Hilfsfunktionen `style_header()` und `auto_width()` nutzen)

### Neue Analysemethode hinzufügen
→ `analyzer.py`: Neue Methode nach dem `defaultdict`-Pattern der bestehenden Methoden implementieren, dann in `exporter.py` und/oder `drucke_report()` einbinden

---

## .gitignore-Hinweise

Folgende Dateien werden ignoriert und gehören NICHT ins Repository:
- `*.pdf` (Eingabedateien mit Kundendaten)
- `*.xlsx`, `*.csv` (generierte Ausgabedateien, Ausnahme: `examples/*.csv`)
- `*.log`
- Virtual Environments (`venv/`, `.env`)
- IDE-Dateien (`.idea/`, `.vscode/`)
- Build-Artefakte (`dist/`, `build/`, `*.egg-info/`)

---

## Berechtigungen

Claude Code hat volle Berechtigungen ohne Nachfrage für dieses Projekt. Konfiguration in `.claude/settings.json`.
