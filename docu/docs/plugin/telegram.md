# <center>Telegram</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Telegram-Nachrichten für POCSAG-Alarmierungen zu senden. 
Außerdem werden Locations versendet, wenn die Felder `lat` und `lon` im Paket definiert sind. (beispielsweise durch das [Geocoding](../modul/geocoding.md) Modul)

## Unterstütze Alarmtypen
- Pocsag

## Resource
`telegram`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|message|Format der Nachricht||
|botToken|Der Api-Key des Telegram-Bots||
|chatIds|Liste mit Chat-Ids der Empfängers / der Emfänger-Gruppen||

**Beispiel:**
```yaml
  - type: plugin
    name: Telegram Plugin
    res: telegram
    config:
      message: "{RIC}({SRIC})\n{MSG}"
      botToken: "{{ Telegram Bot Token }}"
      chatIds: 
        - "{{ Telegram Chat Id }}"
```

---
## Modul Abhängigkeiten
Aus dem Modul [Geocoding](../modul/geocoding.md) (optional):

- `lat`
- `lon`
  
---
## Externe Abhängigkeiten
- python-telegram-bot
