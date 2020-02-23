# <center>Http</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Http-Anfragen für Alarmierungen zu senden.
Wildcards in den Urls werden automatisch ersetzt.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`http`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|fms|Liste mit Urls für Fms-Alarmierung||
|pocsag|Liste mit Urls für Pocsag-Alarmierung||
|zvei|Liste mit Urls für Zvei-Alarmierung||
|msg|Liste mit Urls für Msg-Alarmierung||

**Beispiel:**
```yaml
  - type: plugin
    name: HTTP Plugin
    res: http
    config:
      pocsag:
        - "http://google.com?q={MSG}"
        - "http://duckduckgo.com?q={MSG}"
      fms:
        - "http://duckduckgo.com?q={LOC}"
```

---
## Abhängigkeiten

- asyncio
- aiohttp

---
## Paket Modifikationen

- keine

---
## Zusätzliche Wildcards

- keine