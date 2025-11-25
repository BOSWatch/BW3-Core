# <center>Multicast</center> 
---

## Beschreibung
Mit diesem Modul können Multicast-Alarme verarbeitet werden. Dabei wird eine Alarmnachricht automatisch an mehrere Empfänger (RICs) verteilt.

### Funktionsweise
Multicast-Alarme funktionieren in zwei bis drei Phasen:

1. **Delimiter-Phase (Optional)**: Ein spezieller Delimiter-RIC markiert den Start eines neuen Multicast-Blocks und löscht vorherige wartende Tone-RICs. Der Delimiter selbst wird nicht als Alarm ausgegeben (automatische Filterung). Diese Phase ist optional - ohne Delimiter werden alle leeren Nachrichten als Tone-RICs behandelt.

2. **Tone-RIC-Phase**: Mehrere RICs empfangen (meist) leere Nachrichten. Diese definieren die Empfänger und "registrieren" sich im Modul als Empfänger für die nächste Multicast-Nachricht.

3. **Text-RIC**: Ein spezieller Message-RIC empfängt die eigentliche Alarmnachricht. Diese wird dann automatisch an alle zuvor gesammelten Tone-RICs verteilt.

**Beispiel:**
```
10:31:16 - RIC: 0123456 SubRIC: 1 Message: (leer)          → Delimiter-RIC
10:31:16 - RIC: 0234567 SubRIC: 4 Message: (leer)          → Empfänger 1
10:31:16 - RIC: 0345678 SubRIC: 3 Message: (leer)          → Empfänger 2
10:31:17 - RIC: 0456789 SubRIC: 1 Message: "B3 WOHNHAUS"   → Message-RIC

Generierte Alarme:
→ RIC: 0234567 SubRIC: 4 Message: "B3 WOHNHAUS"
→ RIC: 0345678 SubRIC: 3 Message: "B3 WOHNHAUS"
```

**Wichtig:** Jeder Empfänger behält seine ursprüngliche SubRIC, da diese oft unterschiedliche Alarmtypen oder Prioritäten repräsentiert.

Das Modul unterstützt:

- Mehrere Startmarker (Delimiter)
- Mehrere Text-RICs
- Netzident-RIC zur Paketfilterung
- Automatische Bereinigung alter Tone-RICs (Fehlerfall: Auto-Clear)
- Active Trigger System zur verlustfreien Paketauslieferung
- Wildcards für spätere Weiterverarbeitung
- Frequenz-basierte Trennung
- Multi-Instanz-Betrieb mit geteiltem Zustand

Hinweis: Der Delimiter-RIC (0123456) wird automatisch gefiltert und nicht ausgegeben.

**Wichtig:** Die Text-RIC (Message-RIC) wird **nicht als separates Paket ausgegeben**. Sie dient nur als Nachrichtenträger, der seinen Text an alle gesammelten Tone-RICs verteilt. Falls keine Tone-RICs vorhanden sind, wird die Text-RIC als `multicastMode: single` ausgegeben.

## Unterstützte Alarmtypen
- POCSAG

## Resource
`multicast`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|autoClearTimeout|Auto-Clear Timeout in Sekunden - Nicht zugestellte Empfänger werden nach dieser Zeit als incomplete ausgegeben|10|
|delimiterRics|Komma-getrennte Liste von Startmarkern, die einen Multicast-Block beginnen (leert sofort vorherige Empfänger und werden automatisch gefiltert wenn konfiguriert)|leer|
|textRics|Komma-getrennte Liste von RICs, die den Alarmtext tragen|leer|
|netIdentRics|Komma-getrennte Liste von Netzwerk-Identifikations-RICs (werden automatisch gefiltert wenn konfiguriert)|leer|
|triggerRic|RIC für das Wakeup-Trigger-Paket (optional, bei leer: dynamisch = erste Tone-RIC)|leer|
|triggerHost|IP-Adresse für Loopback-Trigger|127.0.0.1|
|triggerPort|Port für Loopback-Trigger|8080|

**Achtung:** Zahlen welche führende Nullen enthalten müssen in Anführungszeichen gesetzt werden, z.B. `'0012345'`

### Konfigurationsbeispiel 1: Automatische Delimiter-Erkennung (oder nicht verfügbar im Netzwerk) (= Minimalkonfiguration)
```yaml
- type: module
  res: multicast
  name: Multicast Handler
  config:
    textRics: '0299001,0310001'
```
In diesem Modus werden **alle leeren Nachrichten** als toneRics behandelt (keine `delimiterRics` angegeben).

### Konfigurationsbeispiel 2: Mit Delimiter-Trenner (empfohlen)
```yaml
- type: module
  res: multicast
  name: Multicast Handler
  config:
    autoClearTimeout: 10
    delimiterRics: '0988988'
    textRics: '0299001,0310001'
```
In diesem Modus wird **0988988 als Trenner (= Delimiter)** behandelt und **alle anderen leeren Nachrichten als Empfänger**.

### Konfigurationsbeispiel 3: Mit expliziter Trigger-RIC
```yaml
- type: module
  res: multicast
  name: Multicast Handler
  config:
    autoClearTimeout: 10
    delimiterRics: '0988988'
    textRics: '0299001,0310001'
    triggerRic: '9999999'
    triggerHost: '127.0.0.1'
    triggerPort: 8080
```
Verwendet eine feste RIC (9999999) für das interne Wakeup-Trigger-Paket.

### Konfigurationsbeispiel 4: Mit Netzident-Filterung
```yaml
- type: module
  res: multicast
  name: Multicast Handler
  config:
    autoClearTimeout: 10
    delimiterRics: '0988988'
    textRics: '0299001,0310001'
    netIdentRics: '0000001'
```
Filtert Netzident-Pakete (RIC 0000001) automatisch aus der Weiterverarbeitung.

## Integration in Router-Konfiguration

Das Multicast-Modul sollte **vor** den Plugins platziert werden, damit die generierten Alarme korrekt verarbeitet werden:

```yaml
- name: Router POCSAG
  route:
  - type: module
    res: filter.modeFilter
    name: Filter POCSAG
    config:
      allowed:
        - pocsag
  
  # Multicast-Modul hier einfügen
  - type: module
    res: multicast
    name: Multicast Handler
    config:
      textRics: '0299001,0310001'
      delimiterRics: '0288088'
      autoClearTimeout: 10
  
  # Weitere Module und Plugins
  - type: plugin
    res: mysql
    config:
      # ...
  
  - type: plugin
    res: telegram
    config:
      # ...
```

## Beispielhafte Verwendung in Router-Konfigurationen
Das Multicast-Modul gibt für jedes RIC ein eigenes Paket aus UND generiert für konsistente Verarbeitung Listenfelder.
Dies ermöglicht es, entweder jede RIC einzeln zu verarbeiten oder die Listenfelder für eine gesammelte Ausgabe zu verwenden. Vor der weiteren Verarbeitung in Plugins empfiehlt sich eventuell eine Filterung mittels [RegEx-Filter](regex_filter.md).
Die folgenden Beispiele dienen zur Veranschaulichung der Möglichkeiten des Multicast-Modul in Verbindung mit RegEx-Filter.


### Beispiel (Zusätzliche Wildcards werden noch später in diesem Readme erklärt):
```yaml
router:
- name: Router POCSAG
  route:
  - type: module
    res: filter.modeFilter
    config:
      [...]
  - type: module
    res: filter.doubleFilter
    config:
      [...]
  - type: module
    res: descriptor
    config:
      [...]
  - type: module
    res: multicast
    name: Multicast
    config:
      autoClearTimeout: 10
      delimiterRics: '0123456' # Start eines Multicast-Alarms
      textRics: '9909909'  # Text-RIC
  - type: router
     res: RouterMySQL
  - type: router
    res: RouterTelegram

- name: RouterMySQL
  route:
  - type: module
    res: filter.regexFilter
    name: Filter MySQL
    config:
      - name: "Multicast Mode complete or single"
        checks:
          - field: multicastMode
            regex: ^(complete|single)$
  - type: plugin
    res: mysql
    config:
      [...]

- name: RouterTelegram
  route:
  - type: module
    res: filter.regexFilter
    name: Multicast Recipient Index Filter # 1. Paket, da ist alles drin für einen kombinierten Alarm und ist immer vorhanden
    config:
      - name: "Multicast 1 Paket pro Alarm-Paket"
        checks:
          - field: multicastRecipientIndex
            regex: ^1$
  - type: plugin
    res: telegram
    config:
      message_pocsag: |
        <b>{CNAME}</b>
        {MSG}
        Alarmierte Einheiten [{MCAST_COUNT}]: {DESCRIPTION_LIST}
        RICs: {RIC_LIST}
        {TIME}
    [...]

```

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- keine

---
## Paket Modifikationen

### Hinzugefügte Felder bei Multicast-Alarmen:
- `multicastMode`(string): Beschreibt das Ergebnis der Multicast-Verarbeitung, besitzt einen der Werte:

    - `complete`: Vollständiges Multicast-Packet
    - `incomplete`: Unvollständiges Multicast-Packet (meist fehlt die Text-RIC)
    - `single`: Einzelner, "normaler" Alarm (Tone-RIC = Text-RIC)
    - `control`: Netzwerk-Ident-RIC oder andere Verwaltung-RICs

- `multicastRole` (string): Beschreibt die Rolle dieses Pakets innerhalb des Multicast-Ablaufs, besitzt einen der Werte:

    - `delimiter`: Startmarker-Paket (wird automatisch gefiltert wenn delimiterRics konfiguriert)
    - `recipient`: tatsächlicher Empfänger
    - `single`: Einzelner, "normaler" Alarm (Tone-RIC = Text-RIC)
    - `netident`: Netzwerk-Identifikations-Paket (wird automatisch gefiltert wenn netIdentRics konfiguriert)

- `multicastSourceRic` (string): RIC des ursprünglichen Message-RICs
- `multicastRecipientCount` (string): Anzahl der Empfänger insgesamt
- `multicastRecipientIndex` (string): Index dieses Empfängers (1-N), folgende Logik:

    - Empfänger haben den Index 1 bis n.
    - Delimiter/Singles haben Index 1 (da sie alleinstehen).

- `<FELD>_list` (string): Liste von Werten aus allen Empfänger-RICs für jedes Originalfeld (z.B. ric_list, message_list)

### Veränderte Felder bei Multicast-Alarmen:
- `ric`: Wird durch Empfänger-RIC ersetzt
- `subric`: Wird durch Empfänger-SubRIC ersetzt
- `subricText`: Wird durch Empfänger-SubRIC-Text ersetzt
- `message`: Bei incomplete-Modus leer, sonst Text von Text-RIC

### Rückgabewerte:
- **False**: Paket wurde blockiert (z.B. Delimiter/Netident-Filterung), Router stoppt Verarbeitung
- **Liste von Paketen**: Multicast-Verteilung, Router verarbeitet jedes Paket einzeln
- **None**: Normaler Alarm, Router fährt mit unveränderten Paket fort

---
## Zusätzliche Wildcards

Folgende Wildcards stehen in allen nachfolgenden Plugins zur Verfügung:

|Wildcard|Beschreibung|Beispiel|
|--------|------------|--------|
|{MCAST_SOURCE}|RIC des ursprünglichen Message-RICs|0299001|
|{MCAST_COUNT}|Gesamtanzahl der Empfänger dieses Multicasts.|3|
|{MCAST_INDEX}|Index des Empfängers (1-basiert für Recipients, 0 für Control-Pakete)|0, 1, 2, 3, ...|
|{MCAST_MODE}|Art der Multicast-Verarbeitung durch das Modul|complete, incomplete, single, control|
|{MCAST_ROLE}|Rolle des Pakets im Multicast-Ablauf|recipient, single, delimiter, netident|

## Erweiterung der Listen-Wildcards
Das Modul generiert Wildcards für alle gesammelten Felder (RICs, SubRICs, etc.) in Listenform. Diese sind besonders nützlich, um eine kombinierte Ausgabe (z.B. in Telegram) zu erstellen:

|Wildcard|Beschreibung|Zugrundeliegendes Feld|Beispiel|
|--------|------------|--------|--------|
|{RIC_LIST}|Liste aller RICs der Empfänger (durch Komma getrennt).|ric_list|"0299001, 0299002"|
|{SUBRIC_LIST}|Liste aller SubRICs der Empfänger|subric_list|"4, 3"|
|{DESCRIPTION_LIST}|Liste aller (deskriptiven) Namen der Empfänger.|description_list|"FF Musterstadt, BF Beispiel"|
|{<FELD>_LIST}|Liste der Werte für jedes Originalfeld aus dem Paket|<feld>_list|{FREQUENCY_LIST}, {BITRATE_LIST}|

**Wichtig:** Verwende die **originalen Feldnamen** (z.B. `frequency_list`), nicht die Wildcard-Namen (z.B. ~~`FREQ_list`~~).

### Verwendungsbeispiel in Plugins, z.B. Telegram-Plugin:
```yaml
- type: plugin
  res: telegram
  config:
    message_pocsag: |
      {CNAME}
      {MSG}
      RIC: {RIC} / SubRIC: {SRIC}
      Multicast: {MCAST_INDEX}/{MCAST_COUNT} (Quelle: {MCAST_SOURCE})
      {TIME}
```

---
## Funktionsweise im Detail

### Active Trigger System (Verlustfreie Paketauslieferung)

Das Modul verwendet ein aktives Trigger-System, um sicherzustellen, dass **keine Multicast-Pakete verloren gehen**:

1. **Deferred Delivery**: Bei einem Auto-Clear-Timeout werden die incomplete-Pakete nicht sofort ausgegeben, sondern in einer internen Queue gespeichert.

2. **Wakeup-Trigger**: Das Modul sendet ein spezielles Trigger-Paket via Loopback-Socket (Standard: 127.0.0.1:8080) zurück an den BOSWatch-Server.

3. **Queue-Flush**: Beim Empfang des Trigger-Pakets werden alle gespeicherten Pakete aus der Queue ausgegeben.

**Trigger-RIC Auswahl** (3-stufige Fallback-Kette):
- **Explizit**: Wenn `triggerRic` konfiguriert ist, wird diese RIC verwendet
- **Dynamisch**: Wenn nicht konfiguriert, wird die erste Tone-RIC der aktuellen Gruppe verwendet
- **Fallback**: Falls keine Tone-RICs vorhanden sind (sollte nicht vorkommen), wird "9999999" verwendet

**Beispiel-Ablauf bei Auto-Clear:**
```
10:31:16 - Tone-RIC empfangen (0234567)
10:31:16 - Tone-RIC empfangen (0345678)
10:31:26 - Auto-Clear-Timeout (10s) erreicht
         → Incomplete-Pakete in Queue gespeichert
         → Trigger-Paket via Loopback gesendet (RIC: 0234567)
10:31:26 - Trigger-Paket durch BOSWatch-Server verarbeitet
         → Queue-Flush: Incomplete-Pakete werden ausgegeben
```

**Vorteile:**
- Keine Pakete gehen verloren, auch bei hoher Systemlast
- Saubere Trennung von Verarbeitung und Ausgabe
- Ermöglicht zeitlich versetzte Ausgabe ohne Race Conditions

### Zeitbasierte Verarbeitung

1. **Tone-RIC-Sammlung**: Tone-RICs (meist leere Nachrichten) werden empfangen und gespeichert
2. **Auto-Clear**: Nach `autoClearTimeout` Sekunden ohne Text-RIC werden die Tone-RICs als incomplete ausgegeben (via Trigger-System)
3. **Text-RIC-Verteilung**: Sobald ein Text-RIC empfangen wird, erfolgt die sofortige Verteilung an alle gesammelten Tone-RICs
4. **Hard-Timeout-Cleanup**: Nach 3x `autoClearTimeout` (oder max. 120s) werden veraltete Pakete aus dem Speicher gelöscht (Failsafe)

### Frequenz-Trennung

Das Modul trennt Multicast-Listen nach Frequenzen. Dies verhindert Vermischung von Alarmen verschiedener Sender.

**Beispiel:**
```
Frequenz 173.050 MHz: Tone-RICs [0234567, 0345678]
Frequenz 173.075 MHz: Tone-RICs [0456789, 0567890]
→ Werden getrennt verarbeitet, keine Vermischung möglich
```

### SubRIC-Erhaltung

**Wichtig:** Jeder Empfänger behält seine ursprüngliche SubRIC aus der Tone-RIC-Phase. Dies ist entscheidend, da SubRICs unterschiedliche Bedeutungen haben können, z.B.:

- SubRIC 1 (a): Alarmierung
- SubRIC 2 (b): Information
- SubRIC 3 (c): Probealarm
- SubRIC 4 (d): Sirenenalarm

**Beispiel:**
```
Eingehende Tone-RICs:
- RIC: 0234567 SubRIC: 4  (Sirenenalarm)
- RIC: 0345678 SubRIC: 3  (Probealarm)

Text-RIC: RIC: 0456789 SubRIC: 1 Message: "B3 WOHNHAUS"

Ausgegebene Multicast-Pakete:
→ RIC: 0234567 SubRIC: 4 Message: "B3 WOHNHAUS"  (behält SubRIC 4!)
→ RIC: 0345678 SubRIC: 3 Message: "B3 WOHNHAUS"  (behält SubRIC 3!)
```

### Automatische Filterung

- **Delimiter-Pakete**: Werden automatisch gefiltert (nicht weitergegeben), wenn `delimiterRics` konfiguriert ist
- **Netzident-Pakete**: Werden automatisch gefiltert (nicht weitergegeben), wenn `netIdentRics` konfiguriert ist
- **Filterung nach multicastRole**: Ermöglicht saubere nachgelagerte Verarbeitung ohne manuelle Filter

### Multi-Instanz-Betrieb

Das Modul unterstützt mehrere parallele Instanzen mit geteiltem Zustand:

- **Shared State**: Alle Instanzen teilen sich den Tone-RIC-Speicher (frequenz-basiert)
- **Instance-Specific Timeouts**: Jede Instanz kann eigene `autoClearTimeout`-Werte haben
- **Global Cleanup Thread**: Ein globaler Thread prüft alle Instanzen auf Timeouts
- **Thread-Safe**: Alle Operationen sind thread-sicher mit Locks geschützt