# -*- coding: utf-8 -*-
"""
PDF-Extraktion für Roboterwerk Lieferscheine.
"""

import re
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError(
        "PyMuPDF ist nicht installiert. "
        "Installieren mit: pip install pymupdf"
    )


class LieferscheinExtractor:
    """Extrahiert Daten aus Roboterwerk PDF-Lieferscheinen."""

    # Artikel-Prefixe die erkannt werden
    ARTIKEL_PREFIXE = ['RW_', 'UAV_', 'UAS_', 'X-RW-']

    # Ländercode-Mapping
    LAENDER = {
        'DEU': 'Deutschland',
        'NLD': 'Niederlande',
        'POL': 'Polen',
        'AUT': 'Österreich',
        'CHE': 'Schweiz',
        'FRA': 'Frankreich',
        'BEL': 'Belgien',
        'ITA': 'Italien',
        'ESP': 'Spanien',
        'GBR': 'Großbritannien',
        'LUX': 'Luxemburg',
        'DNK': 'Dänemark',
        'SWE': 'Schweden',
        'NOR': 'Norwegen',
        'FIN': 'Finnland',
        'CZE': 'Tschechien',
        'HUN': 'Ungarn',
        'PRT': 'Portugal',
        'SVN': 'Slowenien',
        'HRV': 'Kroatien',
        'GRC': 'Griechenland',
        'ROU': 'Rumänien',
        'BGR': 'Bulgarien',
        'IRL': 'Irland',
    }

    def __init__(self, pdf_pfad):
        """
        Initialisiert den Extractor.

        Args:
            pdf_pfad: Pfad zur PDF-Datei
        """
        self.pdf_pfad = Path(pdf_pfad)
        self.daten = []

    def extrahiere(self, verbose=True):
        """
        Extrahiert alle Lieferscheindaten aus der PDF.

        Args:
            verbose: Ob Fortschrittsmeldungen ausgegeben werden sollen

        Returns:
            list: Liste von Dictionaries mit Lieferscheindaten

        Raises:
            FileNotFoundError: Wenn die PDF-Datei nicht existiert
        """
        if not self.pdf_pfad.exists():
            raise FileNotFoundError(f"PDF nicht gefunden: {self.pdf_pfad}")

        doc = fitz.open(str(self.pdf_pfad))

        if verbose:
            print(f"Verarbeite {len(doc)} Seiten...")

        for i, page in enumerate(doc):
            text = page.get_text()
            if not text:
                continue

            datensatz = self._extrahiere_seite(text, i + 1)
            if datensatz.get('Lieferschein_Nr'):
                self.daten.append(datensatz)

        doc.close()

        if verbose:
            print(f"Extrahiert: {len(self.daten)} Lieferscheine")

        return self.daten

    def _extrahiere_seite(self, text, seiten_nr):
        """Extrahiert Daten aus einer einzelnen Seite."""
        record = {'Seite': seiten_nr}

        # Lieferschein Nr
        match = re.search(r'Lieferschein\s+(\d+)', text)
        record['Lieferschein_Nr'] = match.group(1) if match else ''

        # Datum (Versanddatum)
        match = re.search(r'Datum\s*\n?\s*(\d{2}\.\d{2}\.\d{4})', text)
        record['Datum'] = match.group(1) if match else ''

        # Kunde Nr
        match = re.search(r'Kunde\s*\n?\s*(\d+)', text)
        record['Kunde_Nr'] = match.group(1) if match else ''

        # Amazon Bestellung
        match = re.search(
            r'Bestellung Nr\.\s+([\d-]+)\s+vom\s+(\d{2}\.\d{2}\.\d{4})',
            text
        )
        record['Amazon_Bestellung'] = match.group(1) if match else ''
        record['Bestelldatum'] = match.group(2) if match else ''

        # Betrag (als float für Berechnungen)
        match = re.search(r'\[DBG amount=([\d,]+)\s*EUR\]', text)
        if match:
            record['Betrag'] = float(match.group(1).replace(',', '.'))
        else:
            record['Betrag'] = 0.0

        # Artikel Nr
        record['Artikel_Nr'] = self._extrahiere_artikel_nr(text)

        # Produkt-Typ
        record['Produkt_Typ'] = self._bestimme_produkt_typ(text)

        # Farbe
        record['Farbe'] = self._extrahiere_farbe(
            text, record.get('Artikel_Nr', '')
        )

        # Menge
        match = re.search(r'(\d)\s*Kennzeichen', text)
        record['Menge'] = int(match.group(1)) if match else 1

        # Land aus E-ID
        record['Land_Code'] = self._extrahiere_land(text)
        record['Land'] = self.LAENDER.get(
            record['Land_Code'], record['Land_Code']
        )

        return record

    def _extrahiere_artikel_nr(self, text):
        """Extrahiert die Artikelnummer aus dem Text."""
        for prefix in self.ARTIKEL_PREFIXE:
            pattern = rf'\n({re.escape(prefix)}[\w_-]+)'
            match = re.search(pattern, text)
            if match:
                artikel = match.group(1)
                # Entferne angehängte Wörter
                artikel = re.sub(
                    r'(Roboterwerk|Drohnen|Flying).*$', '', artikel
                )
                if len(artikel) > 3:
                    return artikel
        return ''

    def _bestimme_produkt_typ(self, text):
        """Bestimmt den Produkttyp anhand des Textes."""
        text_lower = text.lower()

        if 'führerschein' in text_lower or 'kompetenznachweis' in text_lower:
            return 'Führerschein'
        elif 'registrierungsbestätigung' in text_lower:
            return 'Registrierungsbestätigung'
        elif any(x in text_lower for x in ['kennzeichen', 'plakette', 'uav-id']):
            return 'Drohnen-Plakette'
        elif any(x in text_lower for x in ['kartenschuber', 'schutzhülle', 'hülle']):
            return 'Zubehör'
        else:
            return 'Sonstig'

    def _extrahiere_farbe(self, text, artikel_nr):
        """Extrahiert die Farbe aus Text oder Artikelnummer."""
        # Direkte Farbnennung im Text
        farben = [
            ('Silber', 'Silber'),
            ('Schwarz', 'Schwarz'),
            ('Gold', 'Gold'),
            ('Weiß', 'Weiß'),
            (r'\bRot\b', 'Rot'),
            ('Blau', 'Blau'),
        ]

        for pattern, farbe in farben:
            if re.search(pattern, text):
                return farbe

        # Farbe aus Artikelnummer
        if artikel_nr:
            if '_BL' in artikel_nr and 'BLAU' not in artikel_nr:
                return 'Schwarz'
            elif '_RO' in artikel_nr:
                return 'Rot'
            elif '_BLAU' in artikel_nr:
                return 'Blau'
            elif '_NA' in artikel_nr:
                return 'Naturfarben'
            elif '_GR' in artikel_nr:
                return 'Grau'

        return ''

    def _extrahiere_land(self, text):
        """Extrahiert den Ländercode aus der E-ID."""
        laender_codes = '|'.join(self.LAENDER.keys())

        # E-ID Format: DEUxxxxxxxx oder DEU-RP-xxxxxxxx
        match = re.search(
            rf'(?:^|\s|e-ID[:\s]+)({laender_codes})[-]?(?:RP-)?[a-z0-9]{{6,}}',
            text,
            re.IGNORECASE | re.MULTILINE
        )
        if match:
            return match.group(1).upper()

        # Fallback: Suche nach explizitem e-ID Pattern
        match = re.search(
            rf'e-ID[:\s]+({laender_codes})[a-z0-9-]',
            text,
            re.IGNORECASE
        )
        if match:
            return match.group(1).upper()

        # Letzter Fallback
        match = re.search(
            rf'\b({laender_codes})[a-z]{{2,}}[0-9a-z]{{4,}}',
            text,
            re.IGNORECASE
        )
        return match.group(1).upper() if match else ''
