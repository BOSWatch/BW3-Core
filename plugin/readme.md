## Eigene Module und Plugins schreiben

Um ein eigenes Modul oder Plugin zu schreiben, sollte man sich
am besten zuerst einmal das das `template` im entsprechenden Ordner ansehen.
Dies kann als Vorlage für das eigene Plugin genutzt werden.

### 1 Informationen anpassen
- Dateikopf anpassen

### 2 Benötigte Methoden überschreiben
#### 2.1 Modul
Die Modul Basisklasse bietet einige Methoden, welche vom Modul überschrieben werden können.
- `onLoad()` wird direkt beim Import des Moduls ausgeführt
- `doWork(bwPacket)` wird bei der Ausführung aufgerufen
- `onUnload()` wird beim Zerstören der Plugin Modul zum Programmende ausgeführt
#### 2.2 Plugin
Die Plugin Basisklasse bietet einige Methoden, welche vom Plugin überschrieben werden können.
- `onLoad()` wird direkt beim Import des Plugins ausgeführt
- `setup()` wird vor jeder Ausführung gerufen
- `fms(bwPacket)` wird bei einem FMS Paket ausgeführt
- `pocsag(bwPacket)` wird bei einem POCSAG Paket ausgeführt
- `zvei(bwPacket)` wird bei einem ZVEI Packet ausgeführt
- `msg(bwPacket)` wird bei einem Nachrichten Packet ausgeführt
- `teardown()` wird nach jeder Ausführung gerufen
- `onUnload()` wird beim Zerstören der Plugin Instanz zum Programmende ausgeführt

### 3 Konfiguration
#### 3.1 Konfiguration anlegen
Jedes Modul oder Plugin wird in einem Router folgendermaßen deklariert:
```yaml
- type: module              # oder plugin
    name: template_module   # Name der Python Datei
    config:                 # config-Sektion
      option1: value 1
      option2: value 2
        underOption1: value 21
        underOption2: value 22
      list:
      - list 1
      - list 2
```

#### 3.2 Konfiguration nutzen
Wird der Instanz eine Konfiguration übergeben wird diese in `self.config`
abgelegt und kann folgendermaßen abgerufen werden:
- `self.config.get("option1")` einzelnes Feld
  - liefert `value 1`
- `self.config.get("option2", "underOption1")` verschachteltes Feld (beliebig viele möglich)
  - liefert `value 21`
- `self.config.get("notSet", default="defValue")` Es kann ein Default Wert angegeben werden (wenn Eintrag in Config fehlt)
  - liefert `defValue`
- `for item in self.config.get(FIELD):` Über Listen kann iteriert werden
  - liefert ein Element je Durchgang - hier `list1` und `list2`

Wird ein End-Wert ausgelesen, wird dieser direkt zurück gegeben.
Sollten weitere Unterelemente oder eine Liste exisitieren
wird erneut ein Element der Klasse `Config()` zurück gegeben

### 4 Arbeiten mit dem bwPacket
An das Modul bzw. Plugin wird eine Instanz eines BOSWatch-Packet Objekts übergeben.

Aus dieser kann mittels `bwPacket.get(FIELDNAME)` das entsprechende Feld
ausgelesen werden. 

Mittels `bwPacket.set(FIELDNAME, VALUE)` kann es hinzugefügt/modifiziert werden. 

Eine Auflistung der bereitgestellten Informationen
findet sich im entsprechenden BOSWatch-Packet Dokument.

#### 4.1 Zu beachten bei Module
Module können Pakete beliebig verändern.
Diese Änderungen werden im Router entsprechend weitergeleitet.

Mögliche Rückgabewerte eines Moduls:
- `return bwPacket` gibt das modifizierte bwPacket an den Router zurück
- `return None` Router fährt mit dem unveränderten bwPacket fort (Input = Output)
- `return False` Router stopt sofort die Ausführung (zB. in Filter verwendet)
#### 4.2 Zu beachten bei Plugins
Plugins geben keine Pakete mehr zurück. Sie fungieren ausschließlich als Endpunkt.
Die Plugin Basisklasse liefert intern immer ein `None` an den Router.
 
### 5 Wildcards parsen (NUR PLUGIN)
Das parsen der Wildcars funktioniert komfortabel über die interne Methode `self.parseWildcards(MSG)`.
Die Platzhalter für die Wildcards findet man in `boswatch/utils/wildcard.py` oder in der `packet.md`.
