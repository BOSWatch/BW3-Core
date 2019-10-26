# <center>Eigenes Modul/Plugin schreiben</center> 

Um ein eigenes Modul oder Plugin zu schreiben, sollte man sich am besten zuerst einmal das das `template` im entsprechenden Ordner ansehen. Dies kann als Vorlage für das eigene Modul oder Plugin genutzt werden.

---
## Allgemeine Informationen
Im ersten Schritt sollte eine Kopie des jeweiligen Templates (Modul oder Plugin) erstellt werden. Nun sollten im Dateikopf die Angaben angepasst werden.

---
## Benötigte Methoden überschreiben
### Modul
Die Modul Basisklasse bietet einige Methoden, welche vom Modul überschrieben werden können.

- `onLoad()` wird direkt beim Import des Moduls ausgeführt
- `doWork(bwPacket)` wird bei der Ausführung aufgerufen
- `onUnload()` wird beim Zerstören der Plugin Modul zum Programmende ausgeführt

### Plugin
Die Plugin Basisklasse bietet einige Methoden, welche vom Plugin überschrieben werden können.

- `onLoad()` wird direkt beim Import des Plugins ausgeführt
- `setup()` wird vor jeder Ausführung gerufen
- `fms(bwPacket)` wird bei einem FMS Paket ausgeführt
- `pocsag(bwPacket)` wird bei einem POCSAG Paket ausgeführt
- `zvei(bwPacket)` wird bei einem ZVEI Packet ausgeführt
- `msg(bwPacket)` wird bei einem Nachrichten Packet ausgeführt
- `teardown()` wird nach jeder Ausführung gerufen
- `onUnload()` wird beim Zerstören der Plugin Instanz zum Programmende ausgeführt

---
## Konfiguration
### Konfiguration anlegen
Jedes Modul oder Plugin wird in einem Router folgendermaßen deklariert:
```yaml
- type: module              # oder 'plugin'
  res: template_module      # Name der Python Datei (ohne .py)
  name: Mein Modul          # optionaler Name
  config:                   # config-Sektion
    option1: value 1
    option2:
      underOption1: value 21
      underOption2: value 22
    list:
      - list 1
      - list 2
```
Eine entsprechende Dokumentation der Parameter **muss** in der Dokumentation des jeweiligen Moduls oder Plugins hinterleget werden.

### Konfiguration verwenden
Wird der Instanz eine Konfiguration übergeben wird diese in `self.config` abgelegt und kann wie folgt abgerufen werden:  
(Dies Ergebnisse beziehen sich auf das Konfigurationsbeispiel oben)

- Einzelnes Feld auslesen  
`self.config.get("option1")`
> liefert `value 1`

- Verschachteltes Feld auslesen (beliebige tiefe möglich)  
`self.config.get("option2", "underOption1")`
> liefert `value 21`

- Es kann ein Default Wert angegeben werden (falls entsprechender Eintrag fehlt)  
`self.config.get("notSet", default="defValue")` 
> liefert `defValue`

 - Über Listen kann einfach iteriert werden  
`for item in self.config.get(FIELD):`
> liefert ein Element je Iteration - hier `list 1` und `list 2`

Wird ein End-Wert ausgelesen, wird dieser direkt zurück gegeben.  
Sollten weitere Unterelemente oder eine Liste exisitieren wird erneut ein Objekt der Klasse `Config()` zurück gegeben, auf welches wiederum nach obigem Schema zugegriffen werden kann.

---
## Arbeiten mit dem bwPacket
An das Modul bzw. Plugin wird eine Instanz eines BOSWatch-Paket Objekts übergeben.  
Aus dieser kann mittels `bwPacket.get(FIELDNAME)` das entsprechende Feld ausgelesen werden.  
Mittels `bwPacket.set(FIELDNAME, VALUE)` kann ein Wert hinzugefügt oder modifiziert werden.  
Eine Auflistung der bereitgestellten Informationen findet sich im entsprechenden [BOSWatch Paket](packet.md) Dokumentation.

**Bitte beachten:**

- Selbst vom Modul hinzugefügte Felder **müssen** in der Modul Dokumentation unter `Paket Modifikation` aufgeführt werden.
- Sollte ein Modul oder Plugin Felder benutzen, welche in einem anderen Modul erstellt werden, **muss** dies im Punkt `Abhänigkeiten` des jeweiligen Moduls oder Plugins dokumentiert werden.

### Rückgabewert bei Modulen
Module können Pakete beliebig verändern. Diese Änderungen werden im Router entsprechend weitergeleitet.

Mögliche Rückgabewerte eines Moduls:

- `return bwPacket` Gibt das modifizierte bwPacket an den Router zurück (Paket Modifikation)
- `return None` Der Router fährt mit dem unveränderten bwPacket fort (Input = Output)
- `return False` Der Router stopt sofort die Ausführung (zB. in Filtern verwendet)

### Rückgabewert bei Plugins
Plugins geben keine Pakete mehr zurück. Sie fungieren ausschließlich als Endpunkt.  
Die Plugin Basisklasse liefert intern immer ein `None` an den Router zurück,
was zur weiteren Ausführung des Routers mit dem original Paket führt. Daher macht es in Plugins keinen Sinn ein Paket zu modifizieren.
  
---
## Nutzung der Wildcards

Es gibt einige vordefinierte Wildcards welche in der [BOSWatch Paket](packet.md) Dokumentation zu finden sind.

Außerdem sind die folgenden allgemeinen Wildcards definiert:

- `{BR}` - Zeilenumbruch `\r\n`
- `{LPAR}` - öffnende Klammer `(`
- `{RPAR}` - schließende Klammer `)`
- `{TIME}` - Aktueller Zeitstempel im Format `%d.%m.%Y %H:%M:%S`

### Wildcards registrieren [Module]
Module können zusätzliche Wildcards registrieren welche anschließend in den Plugins ebenfalls geparst werden können.
Dies kann über die interne Methode `self.registerWildcard(newWildcard, bwPacketField)` gemacht werden.

- `newWildcard` muss im folgenden Format angegeben werden: `{WILDCARD}`
- `bwPacketField` ist der Name des Feldes im bwPacket - gestezt per `bwPacket.set(FIELDNAME, VALUE)`

**Bitte beachten:**

- Selbst vom Modul registrierte Wildcards **müssen** in der Modul Dokumentation unter `Zusätzliche Wildcards` aufgeführt werden.
 
### Wildcards parsen [Plugins]
Das parsen der Wildcars funktioniert komfortabel über die interne Methode `msg = self.parseWildcards(msg)`.

- `msg` enstrpicht dabei dem String in welchem die Wildcards ersetzt werden sollen

Die Platzhalter der Wildcards findet man in der [BOSWatch Paket](packet.md) Dokumentation.

Sollten Module zusätzliche Wildcards registrieren, findet man Informationen dazu in der jeweiligen Plugin Dokumentation

---
## Richtiges Logging
 tbd ... 
 