# <center>CSV Descriptor</center> 
---

## Beschreibung
Mit diesem Modul wird dem Fahrzeug anhand der RIC eine Bezeichnung aus einer CSV-Datei zugeordnet.

## Unterstütze Alarmtypen
- Pocsag
- weitere folgen

## Resource
`csv_descriptor`

## Konfiguration
Informationen zum Aufbau eines [BOSWatch Pakets](../develop/packet.md)


|Feld|Beschreibung|Default|
|----|------------|-------|
|csvfile|Pfadangabe zur CSV-Datei||
|descrField|Name des Feldes im BW Paket in welchem die Beschreibung gespeichert werden soll (kenner)||
|wildcard|Es wird für das angelegte `descrField` automatisch ein Wildcard registriert|{KENNER}|


**Beispiel:**
```yaml
- type: module
  res: csv_descriptor
  name: CSV Descriptor
  config:
    csvfile: "/opt/boswatch3/csv/poc.csv"
    descrField: kenner
    wildcard: "{KENNER}"
```

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- python-csv

---
## Paket Modifikationen
- Wenn keine Beschreibung vorhanden ist, wird im Feld `descrField` "Unbekannt" hinterlegt

---
## Zusätzliche Wildcards
- {KENNER}
