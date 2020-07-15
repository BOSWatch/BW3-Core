# <center>Double Filter</center> 
---

## Beschreibung
Mit diesem Modul ist es möglich, die Pakete auf Duplikate zu Filtern. Je nach Konfiguration werden doppelte Pakete im aktuellen Router weitergeleitet oder verworfen.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei

## Resource
`filter.doubleFilter`

## Konfiguration
|Feld|Beschreibung|Default|
|----|------------|-------|
|ignoreTime|Zeitfenster für doppelte Pakte in Sekunden|10|
|maxEntry|Maximale Anzahl an Paketen in der Vergleichsliste|20|
|pocsagFields|Liste der Pocsag Felder zum Vergleichen: `ric`, `subric` und/oder `message`|`ric,subric`|

**Beispiel:**
```yaml
- type: module
  res: filter.doubleFilter
  config:
    ignoreTime: 30
    maxEntry: 10
    pocsagFields:
      - ric
      - subric
```

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- keine

---
## Paket Modifikationen
- keine

---
## Zusätzliche Wildcards
- keine

