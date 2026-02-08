# <center>Telegram</center> 
---

## Beschreibung

Dieses Plugin ermöglicht den Versand von Telegram-Nachrichten für verschiedene Alarmierungsarten. Um eine hohe Stabilität im BOS-Betrieb zu gewährleisten, erfolgt der Versand asynchron über eine interne Warteschlange (Queue) mit Überlastschutz.

Das Plugin hält die Vorgaben der Telegram API automatisch ein: Eine integrierte Retry-Logik mit exponentiellem Backoff verhindert Nachrichtenverluste bei temporären Netzwerkproblemen. Zudem werden Nachrichten, die das Telegram-Limit von 4.096 Zeichen überschreiten, automatisch gekürzt. Wenn Standortdaten (lat/lon) vorhanden sind, kann das Plugin diese als native Karte senden (erfordert [Geocoding-Modul](../modul/geocoding.md) und Aktivierung via coordinates).

## Unterstützte Alarmtypen
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
|message_msg|Formatvorlage für MSG-Nachricht|`{MSG}`|
|max_retries|Anzahl Wiederholungsversuche bei Fehlern|5|
|initial_delay|Initiale Wartezeit bei Wiederholungsversuchen|2 [Sek.]|
|max_delay|Maximale Retry-Verzögerung|300 [Sek.]|
|parse_mode|Formatierung ("HTML" oder "MarkdownV2"), !Case-sensitive! Empfehlung: HTML|leer|
|coordinates|Aktiviert die Verarbeitung von Standortdaten|false|

**Beispiel:**
```yaml
  - type: plugin
    name: Telegram Plugin
    res: telegram
    config:
      coordinates: true
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

### parse_mode
Über parse_mode kannst du Telegram-Formatierungen verwenden:

- HTML: `<b>fett</b>`, `<i>kursiv</i>`, `<u>unterstrichen</u>`, `<s>durchgestrichen</s>`, ...
- MarkdownV2: `**fett**`, `__unterstrichen__`, `_italic \*text_` usw.

**Wichtig**: Bei MarkdownV2 werden alle Sonderzeichen innerhalb der Wildcards (wie {MSG}) automatisch escaped. Das verhindert zwar API-Fehler, macht aber eine bewusste Formatierung innerhalb des Funktextes unmöglich.

**Nutze HTML**, wenn du fettgedruckte oder kursive Elemente in deinem Template verwenden möchtest, ohne dass der Inhalt der Nachricht verändert wird.
```yaml
# EMPFOHLEN: HTML für Formatierung
parse_mode: "HTML"
message_pocsag: |
  <b>POCSAG Alarm:</b>
  RIC: {RIC}
  {MSG}

# NICHT EMPFOHLEN: MarkdownV2 
# (alle Sonderzeichen in {MSG} werden escaped)
parse_mode: "MarkdownV2"
message_pocsag: "*Alarm*\nRIC: {RIC}"
```

Block-Strings (|) eignen sich perfekt für mehrzeilige Nachrichten und vermeiden Escape-Zeichen wie \n

### coordinates
Der Versand von Standorten ist standardmäßig deaktiviert (`coordinates: false`), um unnötige Warnmeldungen im Log zu vermeiden, wenn keine Koordinaten im Datenpaket enthalten sind. Setze diesen Wert nur auf `true`, wenn du sicherstellst, dass die Alarmierung Koordinaten liefert (z.B. durch einen vorgeschalteten Geocoder).

**Verhalten beim Standortversand:**
Bei aktivierten Koordinaten sendet das Plugin zusätzlich zum Alarmtext eine native Telegram-Karte als separate Nachricht. Es sind keine Wildcards im Nachrichtentext erforderlich; die Karte wird automatisch unter dem Text gepostet.

---
## Modul Abhängigkeiten
OPTIONAL, nur für POCSAG-Locationversand: Aus dem Modul [Geocoding](../modul/geocoding.md):

- `lat`
- `lon`

---
## Externe Abhängigkeiten
requests
