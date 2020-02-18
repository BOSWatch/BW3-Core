# <center>Telegram</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Telegram-Nachrichten für POCSAG-Alarmierungen zu senden.
Außerdem unterstützt das Plugin das Versenden von Location über folgende geocoding-Api's:

- Mapbox
- Google Maps

## Resource
`telegram`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|name|Beliebiger Name des Plugins||

#### `config:`

|Feld|Beschreibung|Default|
|----|------------|-------|
|botToken|Der Api-Key des Telegram-Bots||
|chatId|Die Chat-Id des Empfängers / der Emfänger-Gruppe||
|geocoding|Aktivieren des Geocodings|false|
|geoRegex|Regex Capture-Group zum Herausfiltern der Adresse||
|geoApiProvider|Der Provider für das Geocoding||
|geoApiToken|Der Api-Token fuer die Geocoding-Api||

#### Verfügbare Geocoding Provider

|Name|Einstellungswert|
|----|------------|
|Mapbox|mapbox|
|Google Maps|google|

**Beispiel:**
```yaml
  - type: plugin
    name: Telegram Plugin
    res: telegram
    config:
      botToken: {{ Telegram Bot Token }}
      chatId: {{ Telegram Chat Id }}
      geocoding: true
      geoRegex: ((?:[^ ]*,)*?)
      geoApiProvider: mapbox
      geoApiToken: {{ Mapbox Api Key }}
```

---
## Abhängigkeiten

- python-telegram-bot
- geocoder

---
## Paket Modifikationen

- keine

---
## Zusätzliche Wildcards

- keine
