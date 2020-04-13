# <center>Mode Filter</center> 
---

## Beschreibung
Mit diesem Modul ist es möglich, die Pakete auf bestimmte Modes (FMS, POCSAG, ZVEI) zu Filtern. Je nach Konfiguration werden Pakete eines bestimmten Modes im aktuellen Router weitergeleitet oder verworfen.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`filter.modeFilter`

## Konfiguration
|Feld|Beschreibung|Default|
|----|------------|-------|
|allowed|Liste der erlaubten Paket Typen `fms` `zvei` `pocsag` `msg`||

**Beispiel:**
```yaml
- type: module
  res: filter.modeFilter
  config:
    allowed:
      - fms
      - pocsag
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

