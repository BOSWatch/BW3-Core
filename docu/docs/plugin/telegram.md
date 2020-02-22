# <center>Telegram</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Telegram-Nachrichten für POCSAG-Alarmierungen zu senden. 
Außerdem werden Locations versenden, wenn die Felder `lat` und `lon` im Paket definiert sind. (beispielsweise durch das Geocoding-Modul)


## Unterstütze Alarmtypen
- Pocsag

## Resource
`telegram`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|botToken|Der Api-Key des Telegram-Bots||
|chatIds|Liste mit Chat-Ids der Empfängers / der Emfänger-Gruppen||

**Beispiel:**
```yaml
  - type: plugin
    name: Telegram Plugin
    res: telegram
    config:
      botToken: "{{ Telegram Bot Token }}"
      chatIds: 
        - "{{ Telegram Chat Id }}"
```

---
## Abhängigkeiten

- python-telegram-bot

---
## Paket Modifikationen

- keine

---
## Zusätzliche Wildcards

- keine
