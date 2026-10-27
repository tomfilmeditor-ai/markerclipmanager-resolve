MarkerClipManager — Timeline- und Clip-Marker-Manager für DaVinci Resolve
=========================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.7
MIT License — see the script header

FUNKTION
--------
Ein einziges Fenster zum Anzeigen und Verwalten aller Marker in einer Resolve-Timeline: sowohl
Lineal-Marker (Timeline-Ebene) als auch Marker auf einzelnen Clips auf
allen Video- und Audiospuren.

Für jeden Marker werden angezeigt: Marker-Grafik (gleiche native Form wie Resolve),
Spur, TC Anfang, TC Ende, Dauer, Farbe, Name, Stichwort, Notiz.

FUNKTIONEN
----------
- Wählen Sie einen oder mehrere Marker aus und ändern Sie Farbe oder Spur
  (auch zum/vom "TIMELINE"-Lineal) oder löschen Sie sie
- Bearbeiten Sie Name, Stichwort und Notiz direkt in der Tabelle (Doppelklick),
  auch für mehrere ausgewählte Marker gleichzeitig
- Die Entf-Taste bewirkt dasselbe wie die Schaltfläche Löschen, mit einer
  Bestätigung, die Sie abschalten können
- Rückgängig und Wiederherstellen mit Cmd+Z / Strg+Z, dazu ein History-Fenster:
  Doppelklick auf einen früheren Schritt führt direkt dorthin zurück. Das gilt
  nur für die laufende Sitzung und wird beim Schließen des Skripts geleert
- Filtern nach Farbe, Spur, Autor/Name oder Stichwort
- Marker als CSV exportieren und importieren
- Klick auf eine Zeile: der Abspielkopf springt zu diesem Marker
- Oberfläche in 12 Sprachen: Sie startet in Ihrer Systemsprache, sofern
  vorhanden, sonst auf Englisch, und lässt sich über das Menü oben im Fenster
  umstellen (wirksam nach einem Neustart des Skripts)

ANFORDERUNGEN
-------------
- DaVinci Resolve 19/20 (macOS)
- Python 3 auf dem System installiert
- PySide6 (wird automatisch vom Setup-Skript unten installiert — keine
  manuellen Schritte erforderlich)

INSTALLATION (einmalig)
-----------------------
1. Laden Sie den Installer für Ihr System herunter
2. macOS: RECHTSKLICK auf die .command-Datei und "Öffnen" wählen — kein
   Doppelklick, den macOS blockiert, weil die Datei nicht mit einem
   Apple-Entwicklerzertifikat signiert ist
   Windows: Doppelklick auf die .cmd-Datei; wenn SmartScreen warnt, wählen Sie
   "Weitere Informationen" und dann "Trotzdem ausführen"
3. Der Installer kopiert die Dateien und richtet anschließend die
   Python-Umgebung ein, die das Skript benötigt (dieser Teil braucht eine
   Internetverbindung und dauert etwa eine Minute)
4. Falls dieser zweite Teil fehlschlägt — keine Verbindung oder kein Python —
   sind die Dateien trotzdem korrekt installiert: Öffnen Sie den
   Installationsordner und führen Sie "MarkerClipManager_Setup.command" (macOS)
   bzw. "MarkerClipManager_Setup_Windows.cmd" (Windows) aus, sobald es möglich
   ist
5. Fertig. Aktualisierungen werden genauso installiert, über die vorherige
   Version, und Ihre Einstellungen bleiben unangetastet

VERWENDUNG
----------
In DaVinci Resolve: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(das Skript befindet sich im Unterordner "MarkerClipManager" innerhalb von Comp, daher wird es
im Menü als Untermenü mit demselben Namen angezeigt)

BEKANNTE EINSCHRÄNKUNGEN
------------------------
- Der Marker in der Tabelle ist ein vom Skript erstelltes Symbol, nicht
  das offizielle Symbol von Resolve (nicht von der API zugänglich). Farben sind die genauen
  Hexadezimalwerte des Benutzers — nur die Symbolform bleibt eine
  Approximation
- "Stichwort" ist kein natives Resolve-Marker-Feld: es wird in einem
  internen Marker-Feld (customData) gespeichert, unsichtbar für Resolves natives
  Marker-Panel — nur von diesem Skript lesbar/schreibbar
- Timecode liest fps und Drop Frame/Non-Drop Frame-Modus direkt aus der
  aktiven Timeline des Projekts (29.97 und 59.94 DF werden korrekt mit dem
  Standard-SMPTE-Algorithmus behandelt); bei nicht-standardem fps bleiben die Berechnungen
  ungefähr
- EDL-Import/Export wird von diesem Skript nicht verwaltet: verwenden Sie Resolves natives
  Feature (Timeline > Markers > Export/Import)
- Das Verschieben eines Markers auf eine Video-/Audiospur erfordert, dass bereits ein Clip
  an dieser Position vorhanden ist

UNTERSTÜTZUNG
-------------
Fehlerberichte: Verwenden Sie die 🐛 Schaltfläche in der App (öffnet eine vorgefüllte E-Mail an
tomfilmeditor.tools@gmail.com)
Wenn Sie die Entwicklung unterstützen möchten: ☕ Schaltfläche in der App oder
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
