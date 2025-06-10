# <center>Telegram</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Telegram-Nachrichten für POCSAG-Alarmierungen zu senden. 
Außerdem werden Locations versendet, wenn die Felder `lat` und `lon` im Paket definiert sind. (beispielsweise durch das [Geocoding](../modul/geocoding.md) Modul)

Die abarbeitung der Alarmierungen erfolgt per Queue nach den Limits der Telegram API, damit keine Nachrichten verloren gehen, diese Funktion kann mit dem ```queue``` Parameter deaktiviert werden.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`telegram`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|botToken|Der Api-Key des Telegram-Bots||
|chatIds|Liste mit Chat-Ids der Empfängers / der Emfänger-Gruppen||
|startup_message|Nachricht, dass das Telegram-Plugin erfolgreich geladen wurde|leer|
|message_fms|Format der Nachricht für FMS|`{FMS}`|
|message_pocsag|Format der Nachricht für Pocsag|`{RIC}({SRIC})\n{MSG}`|
|message_zvei|Format der Nachricht für ZVEI|`{TONE}`|
|message_msg|Format der Nachricht für MSG||
|max_retries|Anzahl der Versuche, bis das Senden abgebrochen wird|5|
|initial_delay|Verzögerung des zweiten Sendeversuchs|2 [Sek.]|
|max_delay|Maximale Verzögerung|60 [Sek.]|

**Beispiel:**
```yaml
  - type: plugin
    name: Telegram Plugin
    res: telegram
    config:
      message_pocsag: "{RIC}({SRIC})\n{MSG}"
      startup_message: "Server up and running!"
      botToken: "BOT_TOKEN"
      chatIds:
        - "CHAT_ID"
```

---
## Modul Abhängigkeiten
Aus dem Modul [Geocoding](../modul/geocoding.md) (optional/nur POCSAG):

- `lat`
- `lon`
  
---
## Externe Abhängigkeiten
- python-telegram-bot
