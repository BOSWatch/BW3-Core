# <center>Telegram</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Telegram-Nachrichten für POCSAG-Alarmierungen zu senden. 
Außerdem werden Locations versenden, wenn die Felder `lat` und `lon` im Paket definiert sind. (beispielsweise durch das Geocoding-Modul)

## Externe Abhängigkeiten
- python-telegram-bot

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
## Abhängigkeiten

- keine
