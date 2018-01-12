## Generatoren
Im Verzeichnis `_gen/` befinden sich Windows Batch-Scripte um bestimmt Aufgaben zu
vereinfachen und zu automatisieren.

---

### cloc.bat
`CLoC` steht für Count Lines of Code

Dieses Tool erstellt einen kurzen Report über die Anzahl der Dateien, Codezeilen,
Kommentare und Leerzeilen sortiert nach jeweiliger Programmiersprache

---

### doxygen.bat
Doxygen ist ein Dokumentationswerkzeug zum automatischen dokumentieren von Quellcode.

Nach dem ausführen wird der gesamte Quellcode geparst und eine HTML Dokumentation
im Verzeichnis `_docu/html/` angelegt.

Die Konfigurations Datei für Doxygen findet sich unter `_gen/doxygen.ini`

---

### pytest.bat
pytest ist ein Python Testframework

Damit ist es möglich, automatisierte Tests laufen zu lassen.
Vorher müssen die benötigten Plugins welche unter `_info/requirements.txt` gelistet sind
mittels `pip` installiert werden.

Nach dem Start kann man mit einem Druck auf `[ENTER]` direkt alle bekannten Tests
laufen lassen, oder durch die Eingabe eines spezifischen Tests auch nur diesen
ausführen. Die Tests werden dabei in zufälliger Reihenfolge abgearbeitet um auch
Fehler durch Abhängigkeiten voneinander zu erfassen.

Die Testfälle befinden sich im Unterordner `test/`
Einzeltests werden durch Eingabe des Namens ohne `test_` und `.py` aufgerufen.
Zum Beispiel `decoder` statt `test_decoder.py`

Zusätzlich werden alle Quellcode Dateien mittels eines PEP8 Parsers auf die Einhaltung
der Code-Sytel Vorgaben von Python hin untersucht und etwaige Fehler ausgegeben.

Vom Testverlauf wird ein Logfile erstellt welches in `log/test.log` befindet.

Die Konfigurationsdatei für pytest findet sich unter `_gen/pytest.ini`
