# <center>Konfiguration</center>

Die Konfiguration von BOSWatch 3 ist im YAML Format abgelegt und wird nachfolgend beschrieben.  
Immer wenn für eine Einstellung ein **Default** Wert angegeben ist, muss diese Einstellung nicht
zwingend in die Konfiguration eingetragen werden.

## Client

---
### `client:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|name|Name zur Identifizierung der Client Instanz||
|inputSource|Art der zu nutzenden Input Quelle (aktuell nur `sdr`)||
|useBroadcast|Verbindungsdaten per [Broadcast](information/broadcast.md) beziehen|no|

---
### `server:`
Der Abschnitt `server:` wird nur genutzt, wenn `useBroadcast: no` gesetzt ist.  
Ansonsten wird versucht die Verbindungsdaten per Broadcast Paket direkt vom Server zu beziehen.

|Feld|Beschreibung|Default|
|----|------------|-------|
|ip|IP Adresse des Servers|127.0.0.1|
|port|Port des Sever|8080|

**Beispiel:**
```yaml
server:
  ip: 10.10.10.2
  port: 9123
```

---
### `inputSource:`
Aktuell gibt es nur `sdr:` als Input Quelle

#### `sdr:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|device|rtl_fm Device ID|0|
|frequency|Frequenz des Empfängers||
|error|Frequenz Abweichung in ppm|0|
|squelch|Einstellung der Rauschsperre|0|
|gain|Verstärkung des Eingangssignals|100|

**Beispiel:**
```yaml
inputSource:
  sdr:
    device: 0
    frequency: 85.000M
    error: 0
    squelch: 0
    gain: 100
```

---
### `decoder:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|fms|FMS Decoder|no|
|zvei|ZVEI Decoder|no|
|poc512|POCSAG Decoder (Bitrate 512)|no|
|poc1200|POCSAG Decoder (Bitrate 1200)|no|
|poc2400|POCSAG Decoder (Bitrate 2400)|no|

---
## Server
Nachfolgend alle Paramater der Server Konfiguration

### `server:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|port|Port auf dem der Server lauscht|8080
|name|Name zur Identifizierung der Server Instanz||
|useBroadcast|Verbindungsdaten per Broadcast Server bereitstellen|no|

---
### `alarmRouter:`
Enthält eine Liste der Router Namen, welche bei einem Alarm direkt gestartet werden sollen.

**Beispiel:**
```yaml
alarmRouter:
  - Name des Routers
  - ein weiter Router
```

---
### `router:`
Mit den Routern kann der Verarbeitungsweg eines Alarm-Paketes festgelegt werden. DEs können beliebig viele Router in Form einer Liste angegeben werden.

|Feld|Beschreibung|Default|
|----|------------|-------|
|name|Name des Routers||
|route|Definiten des Routenverlaufs

#### `route:`

Jeder Router kann eine beliebige Anzahl einzelner Routenpunkte enthalten. Diese werden innerhalb des Routers sequentiel abgearbeitet. Mögliche Typen der Routenpunkte sind dabei ein Modul, ein Plugin oder ein anderer Router. Sie werden ebenfalls in Form einer Liste definiert.

|Feld|Beschreibung|Default|
|----|------------|-------|
|type|Art des Routenpunktes (module, plugin, router)||
|name|Zu ladende Resource (Siehe weiter unten)||
|config|Konfigurationseinstellungen des Routenpunktes (Siehe weiter unten)||

**Beispiel:**
```yaml
router:
  - name: Router 1
    route:
      - type: module
        name: filter.modeFilter
        config:
          allowed:
            - fms
```

---
## Module/Plugins

Für die Konfiguration der Module und Plugins ist in den entsprechenden Kategorien eine ausführliche Beschreibung zu finden.
