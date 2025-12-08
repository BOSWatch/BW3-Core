# <center>Descriptor</center> 
---

## Beschreibung
Mit diesem Modul können einem Alarmpaket beliebige Beschreibungen in Abhängigkeit der enthaltenen Informationen hinzugefügt werden.

## Unterstützte Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`descriptor`

## Konfiguration
Informationen zum Aufbau eines [BOSWatch Pakets](../develop/packet.md)

**Achtung:** Zahlen, die führende Nullen enthalten, müssen in der YAML-Konfiguration in Anführungszeichen gesetzt werden, z.B. `'0012345'`. In CSV-Dateien ist dies nicht zwingend erforderlich.

|Feld|Beschreibung|Default|
|----|------------|-------|
|scanField|Feld des BW Pakets, welches geprüft werden soll||
|descrField|Name des Feldes im BW Paket, in welchem die Beschreibung gespeichert werden soll||
|wildcard|Optional: Es kann für das angelegte `descrField` automatisch ein Wildcard registriert werden|None|
|descriptions|Liste der Beschreibungen||
|csvPath|Pfad der CSV-Datei (relativ zum Projektverzeichnis)||

#### `descriptions:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|for|Wert im `scanField`, der geprüft werden soll||
|add|Beschreibungstext, der im `descrField` hinterlegt werden soll||
|isRegex|Muss explizit auf `true` gesetzt werden, wenn RegEx verwendet wird|false|

**Beispiel:**
```yaml
- type: module
  res: descriptor
  config:
    - scanField: tone
      descrField: description
      wildcard: "{DESCR}"
      descriptions:
        - for: 12345
          add: FF DescriptorTest
        - for: '05678' # führende Nullen in '' !
          add: FF TestDescription
        - for: '890(1[1-9]|2[0-9])' # Regex-Pattern in '' !
          add: Feuerwehr Wache \\1 (BF)
          isRegex: true
    - scanField: status
      descrField: fmsStatDescr
      wildcard: "{STATUSTEXT}"
      descriptions:
        - for: 1
          add: Frei (Funk)
        - for: 2
          add: Frei (Wache)
        - ...
```

**Wichtige Punkte für YAML-Regex:**
- Apostroph: Regex-Pattern sollten in `'` stehen, um YAML-Parsing-Probleme zu vermeiden
- isRegex-Flag: Muss explizit auf `true` gesetzt werden
- Escaping: Backslashes müssen in YAML doppelt escaped werden (`\\1` statt `\1`)
- Regex-Gruppen: Mit `\\1`, `\\2` etc. können Teile des Matches in der Beschreibung verwendet werden

#### `csvPath:`

**Beispiel:**
```
- type: module
  res: descriptor
  config:
    - scanField: tone
      descrField: description
      wildcard: "{DESCR}"
      csvPath: "config/descriptions_tone.csv"
```

`csvPath` gibt den Pfad zu einer CSV-Datei an, relativ zum Projektverzeichnis (z. B. `"config/descriptions_tone.csv"`).

Eine neue CSV-Datei (z. B. `descriptions_tone.csv`) hat folgendes Format:

**Beispiel**
```
for,add,isRegex
11111,KBI Landkreis Z,false
12345,FF A-Dorf,false
23456,FF B-Dorf
^3456[0-9]$,FF Grossdorf,true
```

**Hinweis:** In CSV-Dateien müssen Werte mit führenden Nullen **nicht** in Anführungszeichen gesetzt werden (können aber, falls gewünscht). Die Spalte `isRegex` gibt an, ob der Wert in `for` als regulärer Ausdruck interpretiert werden soll (true/false). Falls kein Wert angegeben ist, ist die Paarung standardmäßig `false`, wie z.B. beim Eintrag der FF B-Dorf im obigen Beispiel.

### Kombination von YAML- und CSV-Konfiguration

Beide Varianten können parallel genutzt werden. In diesem Fall werden die Beschreibungen aus der YAML-Konfiguration und aus der angegebenen CSV-Datei in einer gemeinsamen Datenbank zusammengeführt.

#### Matching-Reihenfolge und Priorität

Das Modul wendet folgende Prioritäten beim Matching an:

1. **Exakte Matches** (aus YAML und CSV) werden zuerst geprüft
2. **Regex-Matches** (aus YAML und CSV) werden nur geprüft, wenn kein exakter Match gefunden wurde

**Beispiel für Kombination:**
```yaml
- type: module
  res: descriptor
  config:
    - scanField: tone
      descrField: description
      wildcard: "{DESCR}"
      descriptions:
        - for: 12345
          add: FF YAML-Test (exakt)
        - for: '123.*'
          add: FF YAML-Regex
          isRegex: true
      csvPath: "config/descriptions_tone.csv"
```

Bei einem `scanField`-Wert von `12345` wird **immer** "FF YAML-Test (exakt)" verwendet, auch wenn der Regex ebenfalls zutreffen würde. Regex-Matches werden nur verwendet, wenn kein exakter Match gefunden wurde - unabhängig davon, ob die Einträge aus YAML oder CSV stammen.

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- keine

---
## Paket Modifikationen
- Wenn im Paket das Feld `scanField` vorhanden ist, wird das Feld `descrField` dem Paket hinzugefügt
- Wenn keine Beschreibung vorhanden ist, wird im Feld `descrField` der Inhalt des Feldes `scanField` hinterlegt

---
## Zusätzliche Wildcards
- Von der Konfiguration abhängig