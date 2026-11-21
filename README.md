# ASSISTENTIUM – Website-Prototyp

Klickbarer Prototyp für den Relaunch von assistentium.de (Joomla → WordPress/Divi, Launch Januar 2027).

**Stand:** 21.11.2026 · Ansehen: https://patricia-digital-studio.github.io/assistentium/

## Seiten

| Datei | Inhalt |
| --- | --- |
| `index.html` | Startseite: Hero mit Standbild aus dem Imagefilm, Leistungen, Imagefilm, Leitbild, KOMPASS, Karriere, Aktuelles, Spenden |
| `leistungen.html` | Schulbegleitung, Familienhilfe, Alltagsbegleitung & FED mit Sprungmarken |
| `kompass.html` | KOMPASS by ASSISTENTIUM: Prinzip, für Bewohner, für Wohnungsunternehmen |
| `kreativangebote.html` | Kreativ-Raum, Schreibwerkstatt, Kinder-Kochstube, gemeinsame Infos |
| `karriere.html` | Team, Schulungsprogramm, Benefits, offene Stellen, Bewerbung |
| `aktuelles.html` | Beitragsübersicht (Blog-Design) |
| `beitrag-tannenbaumaktion.html` | Vorlage für einen einzelnen Beitrag |

Kontakt steht auf jeder Seite im Footer.

## Varianten

Unten rechts schaltet der Button **Varianten** zwischen Farbvarianten (Waldgrün, Anthrazit, Hell) und Fließtext-Schriften (Atkinson Hyperlegible, Hind) um. Direktlinks gehen auch: `index.html?farbe=hell&schrift=hind`.

## Bearbeiten

Die Seiten werden aus `tools/pages/*.html` gebaut. Kopf, Navigation und Footer stehen in `tools/build.py`.

```
python3 tools/build.py
```

## Hinweise

- Texte sind sinngemäß nach der alten Website. Im WordPress-Aufbau werden sie aus Joomla übernommen.
- Gestrichelte Kästen sind offene Punkte zur Abstimmung.
- Telefonnummern der Ansprechpartnerinnen sind bewusst Platzhalter.
- Der Imagefilm ist per Zwei-Klick-Lösung über youtube-nocookie.com eingebunden: Vor dem Klick werden keine Daten an YouTube übertragen.
- `noindex` und `robots.txt`: Der Prototyp soll nicht in Suchmaschinen auftauchen.
