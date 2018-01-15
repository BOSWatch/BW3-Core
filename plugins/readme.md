## Eigene Plugins schreiben

Um ein eigenes Plugin zu schrieben, sollte man sich am besten zuerst einmal das Plugin `template` ansehen.
Dies kann als Vorlage für das eigene Plugin genutzt werden.

### 1.) Informationen anpassen
- Dateikopf anpassen
- Namen des Plugins vergeben in der __init__ Methode `super().__init__("template")`

### 2.) Benötigte Methode überschreiben
Die Plugin Basisklasse bietet einige Methoden, welche vom Plugin überschrieben werden können.
- `onLoad()` wird direkt beim Import des Plugins ausgeführt
- `setup()` wird vor jeder Ausführung gerufen
- `fms()` wird bei einem FMS Paket ausgeführt
- `pocsag()` wird bei einem POCSAG Paket ausgeführt
- `zvei()` wird bei einem ZVEI Packet ausgeführt
- `teardown()` wird nach jeder Ausführung gerufen
- `onUnload()` wird beim Zerstören der Plugin Instanz zum Programmende ausgeführt

### 3.) Zugriff auf Config Datei
Wenn sich im Ordner des Plugins eine ini-Datei befindet,
welche exakt so wie das Plugin heißt, kann deren Inhalt
über die lokale Config-Reader Instanz
- `self.config.getBool(SECTION, KEY)`
- `self.config.getInt(SECTION, KEY)`
- `self.config.getStr(SECTION, KEY)`

abgerufen werden.
