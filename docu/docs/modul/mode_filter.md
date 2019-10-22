# <center>Mode Filter</center> 
---

## Beschreibung
Mit diesem Modul ist es Möglich, die Pakete auf bestimmte Modes (FMS, POCSAG, ZVEI) zu Filtern. Je nach Konfiguration werden Pakete eines bestimmten Modes im aktuellen Router weitergeleitet oder verworfen.

## Resource
`filter.modeFilter`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|allowed|Liste der erlaubten Paket Typen `fms` `zvei` `pocsag` `msg`||

**Beispiel:**
```yaml
- type: module
  name: filter.modeFilter
  config:
    allowed:
      - fms
      - pocsag
```

---
## Abhängigkeiten

- keine

---
## Paket Modifikationen

- keine
