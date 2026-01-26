# -*- coding: utf-8 -*-
"""
Verkaufsanalyse für Roboterwerk Lieferscheine.
"""

from collections import defaultdict
from .formatting import DeutscheFormatierung


class VerkaufsAnalyse:
    """Erstellt Verkaufsanalysen aus extrahierten Lieferscheindaten."""

    def __init__(self, daten):
        """
        Initialisiert die Analyse.

        Args:
            daten: Liste von Lieferschein-Dictionaries
        """
        self.daten = daten
        self.fmt = DeutscheFormatierung()

    def zusammenfassung(self):
        """
        Erstellt eine Zusammenfassung der Verkaufsdaten.

        Returns:
            dict: Kennzahlen der Verkaufsdaten
        """
        betraege = [d['Betrag'] for d in self.daten if d.get('Betrag')]

        return {
            'Anzahl_Bestellungen': len(self.daten),
            'Gesamtumsatz': sum(betraege),
            'Durchschnitt': sum(betraege) / len(betraege) if betraege else 0,
            'Minimum': min(betraege) if betraege else 0,
            'Maximum': max(betraege) if betraege else 0,
            'Median': sorted(betraege)[len(betraege)//2] if betraege else 0,
            'Gesamt_Stueck': sum(d.get('Menge', 1) for d in self.daten),
        }

    def nach_produkt_typ(self):
        """
        Gruppiert Daten nach Produkt-Typ.

        Returns:
            dict: Statistiken pro Produkt-Typ
        """
        stats = defaultdict(lambda: {'count': 0, 'umsatz': 0.0, 'stueck': 0})

        for d in self.daten:
            typ = d.get('Produkt_Typ', 'Unbekannt')
            stats[typ]['count'] += 1
            stats[typ]['umsatz'] += d.get('Betrag', 0)
            stats[typ]['stueck'] += d.get('Menge', 1)

        return dict(stats)

    def nach_artikel(self):
        """
        Gruppiert Daten nach Artikel-Nr.

        Returns:
            dict: Statistiken pro Artikel
        """
        stats = defaultdict(lambda: {'count': 0, 'umsatz': 0.0, 'stueck': 0})

        for d in self.daten:
            artikel = d.get('Artikel_Nr') or '(nicht erfasst)'
            stats[artikel]['count'] += 1
            stats[artikel]['umsatz'] += d.get('Betrag', 0)
            stats[artikel]['stueck'] += d.get('Menge', 1)

        return dict(stats)

    def nach_tag(self):
        """
        Gruppiert Daten nach Versanddatum.

        Returns:
            dict: Statistiken pro Tag
        """
        stats = defaultdict(lambda: {'count': 0, 'umsatz': 0.0})

        for d in self.daten:
            tag = d.get('Datum', 'Unbekannt')
            stats[tag]['count'] += 1
            stats[tag]['umsatz'] += d.get('Betrag', 0)

        return dict(stats)

    def nach_farbe(self):
        """
        Gruppiert Daten nach Farbe.

        Returns:
            dict: Statistiken pro Farbe
        """
        stats = defaultdict(lambda: {'count': 0, 'umsatz': 0.0})

        for d in self.daten:
            farbe = d.get('Farbe') or '(keine Angabe)'
            stats[farbe]['count'] += 1
            stats[farbe]['umsatz'] += d.get('Betrag', 0)

        return dict(stats)

    def nach_land(self):
        """
        Gruppiert Daten nach Land.

        Returns:
            dict: Statistiken pro Land
        """
        stats = defaultdict(lambda: {'count': 0, 'umsatz': 0.0})

        for d in self.daten:
            land = d.get('Land') or d.get('Land_Code') or '(nicht erfasst)'
            stats[land]['count'] += 1
            stats[land]['umsatz'] += d.get('Betrag', 0)

        return dict(stats)

    def nach_kunde(self):
        """
        Gruppiert Daten nach Kunde.

        Returns:
            dict: Statistiken pro Kunde
        """
        stats = defaultdict(
            lambda: {'count': 0, 'umsatz': 0.0, 'artikel': []}
        )

        for d in self.daten:
            kunde = d.get('Kunde_Nr', 'Unbekannt')
            stats[kunde]['count'] += 1
            stats[kunde]['umsatz'] += d.get('Betrag', 0)
            if d.get('Artikel_Nr'):
                stats[kunde]['artikel'].append(d['Artikel_Nr'])

        return dict(stats)

    def drucke_report(self):
        """Druckt einen formatierten Report auf der Konsole."""
        fmt = self.fmt
        zf = self.zusammenfassung()

        print("\n" + "=" * 60)
        print("VERKAUFSANALYSE - Roboterwerk GmbH")
        print("=" * 60)

        # Zeitraum ermitteln
        daten_liste = [d['Datum'] for d in self.daten if d.get('Datum')]
        if daten_liste:
            print(f"Zeitraum: {min(daten_liste)} - {max(daten_liste)}")

        print(f"\n{'KENNZAHLEN':^60}")
        print("-" * 60)
        print(f"  Anzahl Bestellungen:      {zf['Anzahl_Bestellungen']:>10}")
        print(f"  Gesamtumsatz:             {fmt.euro(zf['Gesamtumsatz']):>18}")
        print(f"  Durchschnittl. Bestellung:{fmt.euro(zf['Durchschnitt']):>17}")
        print(f"  Minimum:                  {fmt.euro(zf['Minimum']):>18}")
        print(f"  Maximum:                  {fmt.euro(zf['Maximum']):>18}")
        print(f"  Gesamt Stück:             {fmt.zahl(zf['Gesamt_Stueck'], 0):>10}")

        # Nach Produkt-Typ
        print(f"\n{'NACH PRODUKT-TYP':^60}")
        print("-" * 60)
        typ_stats = self.nach_produkt_typ()
        total = len(self.daten)
        for typ, stats in sorted(typ_stats.items(), key=lambda x: -x[1]['umsatz']):
            anteil = stats['count'] / total * 100 if total else 0
            print(
                f"  {typ:25} {stats['count']:>4} ({anteil:>5.1f}%)  "
                f"{fmt.euro(stats['umsatz']):>14}"
            )

        # Nach Artikel (Top 10)
        print(f"\n{'TOP 10 ARTIKEL':^60}")
        print("-" * 60)
        art_stats = self.nach_artikel()
        for i, (art, stats) in enumerate(
            sorted(art_stats.items(), key=lambda x: -x[1]['count'])[:10]
        ):
            print(
                f"  {art:30} {stats['count']:>4}  "
                f"{fmt.euro(stats['umsatz']):>14}"
            )

        # Nach Tag
        print(f"\n{'UMSATZ PRO TAG':^60}")
        print("-" * 60)
        tag_stats = self.nach_tag()
        for tag in sorted(tag_stats.keys(), reverse=True):
            stats = tag_stats[tag]
            print(
                f"  {tag}:  {stats['count']:>4} Bestellungen  "
                f"{fmt.euro(stats['umsatz']):>14}"
            )

        # Nach Land
        print(f"\n{'NACH LAND':^60}")
        print("-" * 60)
        land_stats = self.nach_land()
        for land, stats in sorted(land_stats.items(), key=lambda x: -x[1]['count']):
            anteil = stats['count'] / total * 100 if total else 0
            print(
                f"  {land:20} {stats['count']:>4} ({anteil:>5.1f}%)  "
                f"{fmt.euro(stats['umsatz']):>14}"
            )

        print("\n" + "=" * 60)
