#!/usr/bin/env python3
"""Baut die Prototyp-Seiten aus tools/pages/*.html.

Jede Seitendatei beginnt mit Kopfzeilen im Format `key: value`, dann eine Leerzeile,
dann der Inhalt von <main>. Kopf, Navigation und Footer kommen aus diesem Skript.
Aufruf:  python3 tools/build.py
"""
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "tools" / "pages"
STAND = "21.11.2026"

NAV = [
    ("leistungen", "leistungen.html", "Leistungen"),
    ("kompass", "kompass.html", "KOMPASS"),
    ("kreativangebote", "kreativangebote.html", "Kreativangebote"),
    ("karriere", "karriere.html", "Karriere"),
    ("aktuelles", "aktuelles.html", "Aktuelles"),
]

ARROW = '<span class="arrow" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 20 20"><path d="M3 10h13M11 4l6 6-6 6" stroke="currentColor" stroke-width="2.2" fill="none"/></svg></span>'
PH_TEL = '<span class="ph-tel">[Platzhalter Telefonnummer]</span>'

HEAD = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="icon" href="assets/img/assistentium-logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,700;1,400&family=Hind:wght@400;600;700&family=Montserrat:wght@300;500;700;800&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js"></script>
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<div class="proto-bar" role="note"><div class="wrap"><span><strong>Prototyp</strong> · Stand {stand}</span><span>Texte sinngemäß nach der alten Website, im WordPress-Aufbau übernehmen wir sie aus Joomla</span><span>Gestrichelte Kästen: zur Abstimmung</span></div></div>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html"><img src="assets/img/assistentium-logo.svg" alt="ASSISTENTIUM, zur Startseite" width="1702" height="365"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menü</button>
    <nav id="nav" aria-label="Hauptnavigation">
      <ul>
{nav}
        <li><a class="nav-cta" href="#kontakt">Kontakt</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main" tabindex="-1">
"""

FOOTER = """</main>
<footer class="site-footer" id="kontakt" aria-labelledby="h-kontakt">
  <div class="wrap section">
    <div class="contact-grid">
      <div class="stack">
        <h2 id="h-kontakt"><span class="light">Haben Sie</span> Fragen?</h2>
        <p>Rufen Sie uns gern an. Wir nehmen uns Zeit für Ihr Anliegen.</p>
        <p><strong>ASSISTENTIUM gGmbH</strong><br>Rosengarten 8<br>22880 Wedel</p>
        <p>Telefon <span class="tel">+49 4103 187 17 60</span><br>Mo bis Fr, 8 bis 12 Uhr<br>Fax +49 4103 187 17 58</p>
      </div>
      <div class="stack">
        <ul class="people">
          <li><span class="area">Geschäftsführung · Schulbegleitung · Bewerbungen</span><strong>Berit Johannsen</strong>{ph}</li>
          <li><span class="area">Geschäftsführung · Schulbegleitung · Bewerbungen</span><strong>Sabrina Gollian</strong>{ph}</li>
          <li><span class="area">Alltagsbegleitung &amp; FED</span><strong>Frau Varga-Schicht</strong>{ph}</li>
          <li><span class="area">Büro</span><strong>Anja Heeßel</strong>{ph}</li>
        </ul>
        <p class="proto-note"><strong>Zur Abstimmung:</strong> Ansprechpartnerinnen pro Bereich und Telefonnummern klärt Mel. Für KOMPASS fehlt noch ein Name.</p>
      </div>
    </div>
    <div class="partners" aria-label="Partner und Auszeichnungen">
      <img src="assets/img/aktion-mensch.png" alt="Aktion Mensch: wir unterstützen die Soziallotterie 2026" width="142" height="142">
      <img src="assets/img/iu-praxispartner.png" alt="Offizieller Praxispartner im dualen Studium der IU Internationalen Hochschule" width="110" height="110">
      <img src="assets/img/diingu.png" alt="Offizieller Diingu Weiterbildungspartner" width="316" height="110">
      <img src="assets/img/vdu.jpg" alt="Mitglied im Verband deutscher Unternehmerinnen" width="291" height="120">
    </div>
  </div>
  <div class="legal">
    <div class="wrap">
      <span>© 2026 ASSISTENTIUM gGmbH</span>
      <a href="#kontakt">Impressum</a><a href="#kontakt">Datenschutz</a><a href="#kontakt">Barrierefreiheit</a>
      <span>E-Rechnungen: rechnungen@assistentium.de</span>
      <a href="https://www.instagram.com/assistentium/" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.facebook.com/Assistentium/" target="_blank" rel="noopener">Facebook</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def nav_html(active):
    out = []
    for key, href, label in NAV:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


def build():
    for src in sorted(PAGES.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        head, body = raw.split("\n\n", 1)
        meta = dict(line.split(": ", 1) for line in head.splitlines())
        body = body.replace("{{ARROW}}", ARROW).replace("{{TEL}}", PH_TEL)
        page = HEAD.format(title=html.escape(meta["title"]), description=html.escape(meta["description"]),
                           stand=STAND, nav=nav_html(meta.get("nav", ""))) + body + FOOTER.format(ph=PH_TEL)
        (ROOT / src.name).write_text(page, encoding="utf-8")
        print("gebaut:", src.name)


if __name__ == "__main__":
    build()
