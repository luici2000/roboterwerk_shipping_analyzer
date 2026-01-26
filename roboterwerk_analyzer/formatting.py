# -*- coding: utf-8 -*-
"""
Deutsche Zahlen- und Währungsformatierung.
"""

import locale

# Versuche deutsche Locale zu setzen
try:
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'de_DE')
    except locale.Error:
        pass  # Fallback auf manuelle Formatierung


class DeutscheFormatierung:
    """Hilfklasse für deutsche Zahlen- und Währungsformatierung."""

    @staticmethod
    def zahl(wert, dezimalstellen=2):
        """
        Formatiert eine Zahl nach deutscher Konvention.

        Args:
            wert: Die zu formatierende Zahl
            dezimalstellen: Anzahl der Nachkommastellen (Standard: 2)

        Returns:
            str: Formatierte Zahl (z.B. "1.234,56")

        Example:
            >>> fmt = DeutscheFormatierung()
            >>> fmt.zahl(1234.56)
            '1.234,56'
        """
        if wert is None or wert == '':
            return ''
        try:
            wert = float(wert)
            wert = round(wert, dezimalstellen)

            if dezimalstellen == 0:
                return f"{int(wert):,}".replace(',', '.')
            else:
                ganzzahl = int(wert)
                dezimal = abs(wert - ganzzahl)
                dezimal_str = f"{dezimal:.{dezimalstellen}f}"[2:]
                ganzzahl_str = f"{ganzzahl:,}".replace(',', '.')
                return f"{ganzzahl_str},{dezimal_str}"
        except (ValueError, TypeError):
            return str(wert)

    @staticmethod
    def euro(wert, dezimalstellen=2):
        """
        Formatiert einen Betrag als Euro.

        Args:
            wert: Der zu formatierende Betrag
            dezimalstellen: Anzahl der Nachkommastellen (Standard: 2)

        Returns:
            str: Formatierter Betrag (z.B. "1.234,56 EUR")

        Example:
            >>> fmt = DeutscheFormatierung()
            >>> fmt.euro(1234.56)
            '1.234,56 EUR'
        """
        if wert is None or wert == '':
            return ''
        try:
            wert = float(wert)
            return f"{DeutscheFormatierung.zahl(wert, dezimalstellen)} EUR"
        except (ValueError, TypeError):
            return str(wert)

    @staticmethod
    def prozent(wert, dezimalstellen=1):
        """
        Formatiert einen Wert als Prozent.

        Args:
            wert: Der zu formatierende Wert (0.0 - 1.0)
            dezimalstellen: Anzahl der Nachkommastellen (Standard: 1)

        Returns:
            str: Formatierter Prozentwert (z.B. "12,3 %")

        Example:
            >>> fmt = DeutscheFormatierung()
            >>> fmt.prozent(0.156)
            '15,6 %'
        """
        if wert is None or wert == '':
            return ''
        try:
            wert = float(wert) * 100
            return f"{DeutscheFormatierung.zahl(wert, dezimalstellen)} %"
        except (ValueError, TypeError):
            return str(wert)

    @staticmethod
    def parse_deutsch(text):
        """
        Parst eine deutsche Zahl zu float.

        Args:
            text: Deutsche Zahl als String (z.B. "1.234,56")

        Returns:
            float: Geparster Wert

        Example:
            >>> DeutscheFormatierung.parse_deutsch("1.234,56")
            1234.56
        """
        if not text:
            return 0.0
        try:
            text = str(text).replace('.', '').replace(',', '.')
            return float(text)
        except (ValueError, TypeError):
            return 0.0
