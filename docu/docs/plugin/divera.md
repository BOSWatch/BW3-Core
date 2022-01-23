# <center>Divera 24/7</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Http-Anfragen für Alarmierungen an Divera 24/7 zu senden.
Wildcards in den Urls werden automatisch ersetzt.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`divera`

## Konfiguration
|Feld|Beschreibung|Default|
|----|------------|-------|
|accesskey|Web-API-Schlüssel von Divera24/7 ||
|priority|Sonderrechte|false|
|title| Titel der Meldung | s. Beispiel|
|message| Nachrichteninhalt| s. Beispiel|
|ric|Auszulösende RIC in Divera; Gruppen->Alarmierungs-RIC||
|vehicle|Fahrzeug-Alarmierungs-RIC||

**Beispiel:**
```yaml
  - type: plugin
    name: Divera Plugin
    res: divera
    config:
      accesskey: API-Key
      pocsag:
        priority: false
        title: "{RIC}({SRIC})\n{MSG}"
        message: "{MSG}"
        # RIC ist in Divera definiert
        ric: Probealarm
      fms:
        priority: false
        title: "{FMS}"
        message: "{FMS}"
        vehicle: MTF
     zvei:
       ric: Probealarm
       title: "{TONE}"
       message: "{TONE}"
       priority: false
     msg:
       priority: false
       title: "{MSG}"
       message: "{MSG}"
       # RIC ist in Divera definiert
       ric: Probealarm
      
```

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- asyncio
- aiohttp
- urllib
