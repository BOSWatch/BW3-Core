## Eigene Plugins schreiben

Um ein eigenes Plugin zu schreiben, sollte man sich am besten zuerst einmal das Plugin `template` ansehen.
Dies kann als Vorlage für das eigene Plugin genutzt werden.

### 1.) Informationen anpassen
- Dateikopf anpassen
- Namen des Plugins vergeben in der __init__ Methode `super().__init__("template")`

### 2.) Benötigte Methode überschreiben
Die Plugin Basisklasse bietet einige Methoden, welche vom Plugin überschrieben werden können.
- `onLoad()` wird direkt beim Import des Plugins ausgeführt
- `setup()` wird vor jeder Ausführung gerufen
- `fms(bwPacket)` wird bei einem FMS Paket ausgeführt
- `pocsag(bwPacket)` wird bei einem POCSAG Paket ausgeführt
- `zvei(bwPacket)` wird bei einem ZVEI Packet ausgeführt
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

### 4.) Daten aus dem BOSWatch Paket lesen
An die Alarm Funktionen FMS, POCSAG und ZVEI wird eine Instanz eines
BOSWatch-Packet Objketes übergeben.

Aus dieser kann mittels `bwPacket.get(FELDNAME)` das entsprechende Feld
ausgelesen werden. Eine Auflistung der bereitgestellten Informationen
findet sich im entsprechenden BOSWatch-Packet Dokument.