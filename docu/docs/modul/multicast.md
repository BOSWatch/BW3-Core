# <center>Multicast</center> 
---

## Beschreibung
Das Multicast-Modul verarbeitet komplexe Alarmsequenzen, bei denen eine Nachricht (Text-RIC) an eine Liste zuvor gesendeter Empfänger (Tone-RICs) verteilt wird. Es sorgt dafür, dass jeder Empfänger ein individuelles Paket mit dem Alarmtext erhält.

Das Modul filtert keine inhaltlich relevanten Pakete. Alle Pakete mit Alarminhalt werden mit `multicastRole` markiert und weitergereicht. Die Filterung nach Bedarf erfolgt nachgelagert, z.B. mit `filter.regexFilter`.

Das Modul unterstützt:

- **Multi-Instance Support:** Vollständige Isolation bei parallelem Betrieb in verschiedenen Routen.
- **Frequenz-Trennung:** Verhindert die Vermischung von Alarmen auf unterschiedlichen Kanälen.
- **Active Trigger System:** Nutzt TCP-Loopback, um auch bei Inaktivität des Funkkanals Timeouts sicher zu verarbeiten.
- **Dynamische Listen:** Generiert aggregierte Listenfelder (z. B. {RIC_LIST}) für Sammel-Alarmierungen.
- **Metadaten-Enrichment:** Markiert Pakete präzise für nachgelagerte Filter (z. B. RegEx).

### Funktionsweise
Multicast-Alarme funktionieren in zwei bis vier Phasen:
**Wichtig:** Das Modul arbeitet verzögert bei der Ausgabe der Text-RICs, um die Pakete anzureichern.

1. **Delimiter-Phase (Optional)**: Ein spezieller Delimiter-RIC markiert den Start eines neuen Multicast-Blocks. Er wird als technisches Paket (`multicastRole: delimiter`) **sofort** durchgereicht, leert aber intern den RAM-Puffer für neue Empfänger. Diese Phase ist optional - ohne Delimiter werden alle leeren Nachrichten als Tone-RICs behandelt. Downstream-Filter (z.B. filter.regexFilter) können ihn bei Bedarf ausfiltern.

2. **Tone-RIC-Phase**: Eingehende leere Nachrichten werden **nicht direkt als Pakete ausgegeben**, sondern im RAM zwischengespeichert. Das Modul gibt hier `False` zurück, wodurch der Router die Verarbeitung für dieses spezifische Paket vorerst pausiert.

3. **Text-RIC**: Ein spezieller Message-RIC empfängt die eigentliche Alarmnachricht. Sobald eine Text-RIC empfangen wird, "kopiert" das Modul diesen Text in jedes einzelne der gespeicherten Tone-RIC-Pakete. Diese werden dann als **Liste von Paketen** gesammelt an den Router als `multicastMode: complete` übergeben. Falls keine Tone-RICs im Puffer liegen (z.B. Einzelalarm), wird die Text-RIC als `multicastMode: single` ausgegeben.
**Wichtig:** Die Text-RIC (Message-RIC) wird **nicht als separates Paket ausgegeben**. Sie dient nur als Nachrichtenträger, der seinen Text an alle gesammelten Tone-RICs verteilt. Ausnahme: Einzelalarm (Single)

4. **Timeout-Phase (Auto-Clear - Optional):** Läuft der `autoClearTimeout` ab, ohne dass ein Text-RIC eintrifft, werden die gepufferten RICs als `multicastMode: incomplete` (ohne Text) ausgegeben.

## Unterstützte Alarmtypen
- POCSAG

## Resource
`multicast`

## Konfiguration

|Feld|Beschreibung|Default|
|----|------------|-------|
|autoClearTimeout|Zeit in Sekunden, nach der Tone-RICs ohne Text-Eingang als `incomplete` ausgegeben werden|10|
|delimiterRics|Komma-getrennte Liste von Startmarkern (leert Puffer, `multicastRole: delimiter`)|leer|
|textRics|Komma-getrennte Liste von RICs, die den Alarmtext tragen|leer|
|netIdentRics|Komma-getrennte Liste von Netzwerk-Identifikations-RICs (`multicastRole: netident`)|leer|
|triggerRic|RIC für das Wakeup-Trigger-Paket (optional, bei leer: dynamisch = erste Tone-RIC)|leer|
|triggerHost|IP-Adresse für Loopback-Trigger|127.0.0.1|
|triggerPort|Port für Loopback-Trigger (entspricht meist Server-Port)|8080|

**Hinweis:** Zahlen mit führenden Nullen müssen in Anführungszeichen gesetzt werden, z.B. `'0012345'`.

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
Markiert Netzident-Pakete (RIC 0000001) mit multicastRole: netident. Downstream-Filter können sie gezielt ausfiltern (z.B. RegEx-Filter).

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- keine

---
## Paket Modifikationen

### Hinzugefügte Felder
- `multicastMode`(string): Beschreibt das Ergebnis der Multicast-Verarbeitung, besitzt einen der Werte:
    - `complete`: Vollständiges Multicast-Packet
    - `incomplete`: Unvollständiges Multicast-Packet (meist fehlt die Text-RIC) (Timeout)
    - `single`: Einzelner, "normaler" Alarm (Tone-RIC = Text-RIC)
    - `control`: Netzwerk-Ident-RIC oder andere Verwaltung-RICs (Technik)
- `multicastRole`: 
    - `delimiter`
    - `netident`
    - `recipient` (Empfänger)
    - `single`
- `multicastRecipientIndex` (string): Index dieses Empfängers (1-N), folgende Logik:
    - Bei **recipient**: Zählt hoch (z.B. 1 von 5, 2 von 5...)
    - Bei **delimiter / netident / single**: Immer **1**, da sie als eigenständige technische Pakete zählen
- `multicastRecipientCount` (string): Gesamtanzahl der Empfänger des Multicasts
- `<FELD>_list` (string): Liste von Werten aus allen Empfänger-RICs für jedes Originalfeld (z.B. `ric_list`, `subric_list`)

### Ergänzte Felder (von Text-RIC an Tone-RIC):
- `message`: Der Text wird aus der Text-RIC übernommen und in die Empfänger-Pakete eingefügt (Bei incomplete-Modus leer)
- `multicastSourceRic` (string): RIC des ursprünglichen Message-RICs

### Erhaltene Felder (Tone-RIC):
Diese Felder bleiben **unverändert** bestehen, damit die Zuordnung zum Endgerät korrekt bleibt:
- `ric`
- `subric`
- alle bereits zuvor hinzugefügten Felder (z.B. Descriptor-Modul)

### Rückgabewerte:
- **False**: Paket wurde intern konsumiert (z.B. Tone-RIC wurde in den Buffer aufgenommen), Router stoppt Verarbeitung für dieses Paket (Verhindert die Ausgabe leerer Nachrichten). Allerdings: Das Paket wird im RAM geparkt.
- **Liste von Paketen**: Tritt ein, sobald eine Text-RIC die Verteilung auslöst oder ein Timeout abläuft. Der Router verarbeitet jedes Element der Liste (die nun angereicherten Tone-RICs) als eigenständigen Alarm.
- **None**: Der Router verarbeitet das Original-Paket normal weiter.

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

### Erweiterung der Listen-Wildcards
Das Modul generiert Wildcards für alle gesammelten Felder (RICs, SubRICs, etc.) in Listenform. Diese sind besonders nützlich, um eine kombinierte Ausgabe (z.B. in Telegram) zu erstellen. Im Folgenden ein paar Beispiele:

|Wildcard|Beschreibung|Zugrundeliegendes Feld|Beispiel|
|--------|------------|--------|--------|
|{RIC_LIST}|Liste aller RICs der Empfänger (durch Komma getrennt).|ric_list|"0299001, 0299002"|
|{SUBRIC_LIST}|Liste aller SubRICs der Empfänger|subric_list|"4, 3"|
|{DESCRIPTION_LIST}|Liste aller (deskriptiven) Namen der Empfänger (BEISPIEL! **NUR** bei vorher durchlaufenen Descriptor-Modul)|description_list|"FF Musterstadt, BF Beispiel"|
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
# Funktionsweise im Detail

## Grundsätzliche Funktion

**Beispiel:**
```
10:31:16 - RIC: 0123456 SubRIC: 1 Message: (leer)          → Delimiter-RIC
10:31:16 - RIC: 0234567 SubRIC: 4 Message: (leer)          → Empfänger 1
10:31:16 - RIC: 0345678 SubRIC: 3 Message: (leer)          → Empfänger 2
10:31:17 - RIC: 0456789 SubRIC: 1 Message: "B3 WOHNHAUS"   → Message-RIC

Generierte Alarme:
→ RIC: 0234567 SubRIC: 4 Message: "B3 WOHNHAUS"  (behält SubRIC 4!)
→ RIC: 0345678 SubRIC: 3 Message: "B3 WOHNHAUS"  (behält SubRIC 3!)
```

**Wichtig:** Jeder Empfänger behält seine ursprüngliche SubRIC, da diese oft unterschiedliche Alarmtypen oder Prioritäten repräsentiert.

### Logik der hinzugefügten Felder

Um die Logik der Felder multicastMode, multicastRole, etc. zu verstehen, hilft eine tabellarische Gegenüberstellung:

**1) Szenario Der "Feldstärke-Alarm" (Netident/Delimiter)**

|Paket-Typ|RIC|multicastMode|multicastRole|sourceRic|Index|Count|
|--------|-------|-------|---------|------|--|--|
|Delimiter|0288088|control|delimiter|0288088|1|1|
|Netzident|0000001|control|netident|0000001|1|1|

Hinweis: Diese Pakete dienen der Systemsteuerung. Der Index ist immer 1, da sie "Einzelereignisse" im technischen Ablauf sind.
Beide RIC werden unmittelbar nach der Verarbeitung weitergereicht, d.h. es wird nicht auf die Netzident-RIC gewartet, um die Delmitier-RIC weiterzureichen.

**2) Szenario Echter Multicast-Alarm (Vollständig)**
Hier sieht man den Ablauf: 
- Der Delimiter leert den Speicher und wird mit den ergänzenden Feldern angereichert und sofort weitergegeben.
- Zwei Tone-RICs sammeln sich an
- Die Text-RIC löst die Verteilung aus

**Beachte:** Die Text-RIC (0456789) dient als Nachrichtenträger und erscheint nicht als eigenes Paket im Output.

|Phase|Paket-Typ|RIC|multicastMode|multicastRole|sourceRic|Index|Count|
|-----|---------|---|-------------|-------------|---------|-----|-----|
|Start|Delimiter|0288088|control|delimiter|0288088|1|1|
|Sammler|Tone-RIC 1|0234567|-|(interner Buffer)|-|-|-|
|Sammler|Tone-RIC 2|0345678|-|(interner Buffer)|-|-|-|
|Auslöser|Text-RIC|0456789|(wird verteilt - keine Ausgabe)|(Nachrichtenträger)|-|-|-|
|Output 1|Alarm-Paket|0234567|complete|recipient|0456789|1|2|
|Output 2|Alarm-Paket|0345678|complete|recipient|0456789|2|2|

**3) Szenario Unvollständiger Alarm (Incomplete / Timeout)**
In diesem Fall fehlt die Text-RIC. Das System wartet bis zum Timeout und schickt dann die Empfänger mit leerer Nachricht raus (getriggert durch das Active Trigger System).

|Phase|Paket-Typ|RIC|multicastMode|multicastRole|sourceRic|Index|Count|
|-----|---------|---|-------------|-------------|---------|-----|-----|
|Start|Delimiter|0288088|control|delimiter|0288088|1|1|
|Sammler|Tone-RIC 1|0234567|-|(interner Buffer)|-|-|-|
|Sammler|Tone-RIC 2|0345678|-|(interner Buffer)|-|-|-|
|Event|Timeout|Kein Text|Auto-Clear nach standardmäßig 10s|-|-|-|-|
|Output 1|Incomplete|0234567|incomplete|recipient|0234567|1|2|
|Output 2|Incomplete|0345678|incomplete|recipient|0234567|2|2|

Der Delimiter wird mit den ergänzenden Feldern angereichert und sofort weitergegeben.

---
## Integration in Router-Konfiguration

Das Multicast-Modul muss **vor** den Plugins platziert werden, damit die generierten Alarme korrekt verarbeitet werden:

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


### Beispiel (siehe auch "Zusätzliche Wildcards"):
```yaml
router:
- name: Router POCSAG
  route:
  - type: module
    res: filter.modeFilter
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
  - type: module
    res: filter.doubleFilter
    config:
      [...]
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

## Das Active Trigger System (Verlustfreie Paketauslieferung)
BOSWatch arbeitet **synchron**. Das bedeutet: Der Router "schläft", wenn kein Funk-Paket von außen eingeht. Ein Timeout im Hintergrund-Thread des Moduls kann den schlafenden Router nicht von alleine aufwecken, um die im RAM wartenden Pakete (`incomplete`) herauszuschieben.

**Lösung:** 
Das Modul verwendet ein aktives Trigger-System, um sicherzustellen, dass **keine Multicast-Pakete verloren gehen**

**Ausführung**
Das Modul sendet über via TCP (Loopback) ein minimales Trigger-Paket an den eigenen BOSWatch-Server. Dieser empfängt es wie einen normalen Funk-Alarm, weckt den Router auf und das Modul kann die wartenden Alarme (`incomplete`) sicher ausliefern.

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
2. **Text-RIC-Verteilung**: Sobald ein Text-RIC empfangen wird, erfolgt die sofortige Verteilung an alle gesammelten Tone-RICs
3. **Auto-Clear**: Nach `autoClearTimeout` Sekunden ohne Text-RIC werden die Tone-RICs als incomplete ausgegeben (via Trigger-System)
4. **Hard-Timeout-Cleanup**: Nach 3x `autoClearTimeout` (oder max. 120s) werden veraltete Pakete aus dem Speicher gelöscht (Failsafe)

### Frequenz-Trennung

Das Modul trennt Multicast-Listen nach Frequenzen. Dies verhindert Vermischung von Alarmen verschiedener Sender.

**Beispiel:**
```
Frequenz 173.050 MHz: Tone-RICs [0234567, 0345678]
Frequenz 173.075 MHz: Tone-RICs [0456789, 0567890]
→ Werden getrennt verarbeitet, keine Vermischung möglich (wichtig für Multi-Client mit Single-Server)
```

## Paketmarkierung statt interner Filterung

Das Modul filtert keine inhaltlich relevanten Pakete. 
Alle Pakete werden mit `multicastRole` markiert und weitergereicht. Die Filterung nach Bedarf erfolgt nachgelagert, z.B. mit `filter.regexFilter`.

Eine Ausnahme bilden **Tone-RICs** (leere Nachrichten): Diese werden zuerst intern im Buffer gesammelt und bei einem complete-Alarm (und incomplete) in die Listenfelder aggregiert. Die Listenfelder werden an alle **Tone-RICs** angehängt und anschließend jede **Tone-RIC** angereichert ausgegeben.

Pakete und ihre Rollen:

- **Delimiter-Pakete**: Erhalten `multicastRole: delimiter`
- **Netzident-Pakete**: Erhalten `multicastRole: netident`  
- **Empfänger-Pakete**: Erhalten `multicastRole: recipient`
- **Einzelalarme**: Erhalten `multicastRole: single`

Beispiel-Filter um Delimiter und Netident auszublenden:
```yaml
- type: module
  res: filter.regexFilter
  config:
    - name: "Nur echte Alarme"
      checks:
        - field: multicastRole
          regex: ^(recipient|single)$multicastIndex
```


---

## Zusammenfassung: Was passiert mit den Daten?

- Der Delimiter: Wird sofort markiert und als technisches Paket weitergereicht. Er sorgt dafür, dass keine "Leichen" von alten, abgebrochenen Alarmen im Speicher liegen.
- Die Tone-RICs: Diese werden vom Modul "geschluckt" (return False). Sie verschwinden kurzzeitig aus dem Datenfluss und warten im RAM.
- Die Text-RIC: Wenn sie eintrifft, nimmt das Modul ihren Text (B3 WOHNHAUS) und kopiert ihn in die Tone-RIC-Pakete im RAM. Anschließend erfolgt die Ausgabe der Tone-RICs.
- Die Metadaten: Erst beim Erzeugen der Output-Pakete werden Felder wie multicastRecipientIndex berechnet, damit nachfolgende Plugins wissen, dass diese Pakete zusammengehören.

Technischer Hinweis:
Da die Text-RIC im complete-Fall "verbraucht" wird, um die Tone-RICs zu füllen, wird sie nicht als separates zusätzliches Paket ausgegeben. Das verhindert Dopplungen in der Datenbank. Nur wenn gar keine Tone-RICs da sind, wird die Text-RIC als `single` ausgegeben.
In diesem Fall (Single) ist es völlig egal, ob die Text-RIC mit Delimiter oder ohne empfangen wird - die Delimiter-RIC wird als Delimiter gekennzeichnet, das Text-RIC als Single (in `multicastMode` sowie in `multicastRole`, `multicastRecipientIndex: 1`, `multicastRecipientCount: 1`).

### Multi-Instanz-Betrieb
Das Modul unterstützt unbegrenzte parallele Instanzen durch vollständige Isolation:

- **Encapsulated State:** Jede Instanz verwaltet ihren eigenen Tone-RIC-Speicher. Es gibt keine Vermischung zwischen verschiedenen Routen.
- **Isolated Cleanup:** Jede Instanz startet einen eigenen, internen Cleanup-Thread für präzises Timeout-Management.
- **Instance IDs:** Zur besseren Nachverfolgung im Log erhält jede Instanz eine eindeutige ID (z.B. MCAST_a1b2).
