# <center>Geocoding</center> 
---

## Beschreibung
Mit diesem Modul können einem Paket die Koordinaten eines Ortes oder einer Adresse angefügt werden.

## Unterstützte Alarmtypen
 - Pocsag

## Resource
`geocoding`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
apiProvider|Der Provider für das Geocoding|
apiToken|Der Api-Token fuer die Geocoding-Api|
geoRegex|Regex Capture-Group zum Herausfiltern der Adresse|

#### Verfügbare Geocoding Provider

|Name|Einstellungswert|
|----|------------|
|Mapbox|mapbox|
|Google Maps|google|

**Beispiel:**
```yaml
  - type: module
    name: Geocoding Module
    res: geocoding
    config:
      apiProvider: "{{ Provider für Geocoding }}"
      apiToken: "{{ API-Key für Provider }}"
      regex: "((?:[^ ]*,)*?)"
```

---
## Abhängigkeiten

- geocoder
- re

---
## Paket Modifikationen

- Im Paket werden die Felder `lat` und `lng` hinterlegt

---
## Zusätzliche Wildcards

- keine