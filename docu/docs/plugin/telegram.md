# <center>Telegram</center> 
---

## Beschreibung
Dieses Plugin ermöglicht das Versenden von Telegram-Nachrichten für verschiedene Alarmierungsarten.
Wenn im eingehenden Paket die Felder `lat` und `lon` vorhanden sind (z. B. durch das [Geocoding](../modul/geocoding.md) Modul), wird zusätzlich automatisch der Standort als Telegram-Location gesendet.

Das Senden der Nachrichten erfolgt über eine interne Queue mit Retry-Logik und exponentiellem Backoff, um die Vorgaben der Telegram API einzuhalten und Nachrichtenverluste zu verhindern. Die Retry-Parameter (max_retries, initial_delay, max_delay) können in der Konfiguration angepasst werden.

## Unterstütze Alarmtypen
- FMS
- POCSAG
- ZVEI
- MSG

## Resource
`telegram`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|botToken|Der Api-Key des Telegram-Bots|-|
|chatIds|Liste mit Chat-Ids der Empfängers / der Empfänger-Gruppen|-|
|startup_message|Nachricht beim erfolgreichen Initialisieren des Plugins|leer|
|message_fms|Formatvorlage für FMS-Alarm|`{FMS}`|
|message_pocsag|Formatvorlage für POCSAG|`{RIC}({SRIC})\n{MSG}`|
|message_zvei|Formatvorlage für ZVEI|`{TONE}`|
|message_msg|Formatvorlage für MSG-Nachricht|-|
|max_retries|Anzahl Wiederholungsversuche bei Fehlern|5|
|initial_delay|Initiale Wartezeit bei Wiederholungsversuchen|2 [Sek.]|
|max_delay|Maximale Retry-Verzögerung|300 [Sek.]|
|parse_mode|Formatierung ("HTML" oder "MarkdownV2"), Case-sensitive!|leer|

**Beispiel:**
```yaml
  - type: plugin
    name: Telegram Plugin
    res: telegram
    config:
      message_pocsag: |
        <b>POCSAG Alarm:</b>
        RIC: <b>{RIC}</b> ({SRIC})
        {MSG}
      parse_mode: "HTML"
      startup_message: "Server up and running!"
      botToken: "BOT_TOKEN"
      chatIds:
        - "CHAT_ID"
```

Hinweis:
Über parse_mode kannst du Telegram-Formatierungen verwenden:

- HTML: `<b>fett</b>`, `<i>kursiv</i>`, `<u>unterstrichen</u>`, `<s>durchgestrichen</s>`, ...
- MarkdownV2: `**fett**`, `__unterstrichen__`, `_italic \*text_` usw. (Escape-Regeln beachten)

Block-Strings (|) eignen sich perfekt für mehrzeilige Nachrichten und vermeiden Escape-Zeichen wie \n

---
## Modul Abhängigkeiten
OPTIONAL, nur für POCSAG-Locationversand: Aus dem Modul [Geocoding](../modul/geocoding.md):

- `lat`
- `lon`
  
---
## Externe Abhängigkeiten
keine
