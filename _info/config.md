## Konfiguration

Die Konfiguration von BOSWatch 3 ist im YAML Format abgelegt und wird nachfolgend beschrieben.
Immer wenn für eine Einstellung ein **Default** Wert angegeben ist, muss diese Einstellung nicht
zwingend in die Konfiguration eingetragen werden.


### Client

#### `client:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|name|Name zur Identifizierung der Client Instanz||
|inoutSource|Art der zu nutzenden Input Quelle (aktuell nur `sdr`)||
|useBroadcast|Verbindungsdaten per Broadcast beziehen|no|

#### `server:`
Der Abschnitt `server:` wird nur genutzt, wenn `useBroadcast: no` gesetzt ist.

|Feld|Beschreibung|Default|
|----|------------|-------|
|ip|IP Adresse des Servers|127.0.0.1|
|port|Port des Sever|8080|

#### `inputSource:`
Aktuell gibt es nur `sdr:` als Input Quelle

##### `sdr:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|device|rtl_fm Device ID|0|
|frequency|Frequenz des Empfängers||
|error|Frequenz Abweichung in ppm|0|
|squelch|Einstellung der Rauschsperre|0|
|gain|Verstärkung des Eingangssignals|100|

Bsp:
```yaml
inputSource:
  sdr:
    device: 0
    frequency: 85.000M
    error: 0
    squelch: 0
    gain: 100
```

#### `decoder:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|fms|FMS Decoder|no|
|zvei|ZVEI Decoder|no|
|poc512|POCSAG Decoder (Bitrate 512)|no|
|poc1200|POCSAG Decoder (Bitrate 1200)|no|
|poc2400|POCSAG Decoder (Bitrate 2400)|no|

---
### Server

#### `server:`
|Feld|Beschreibung|Default|
|----|------------|-------|
|port|Port auf dem der Server lauscht|8080
|name|Name zur Identifizierung der Server Instanz||
|useBroadcast|Verbindungsdaten per Broadcast Server bereitstellen|no|

#### `alarmRouter:`
Enthält eine Liste der Router Namen, welche bei einem Alarm direkt gestartet werden sollen.

Bsp:
```yaml
alarmRouter:
- Name des Routers
- ein weiter Router
```

#### `router:`
Mit den Routern kann der Verarbeitungsweg eines Alarm-Paketes festgelegt werden.
Diese werden als Liste angegeben

|Feld|Beschreibung|Default|
|----|------------|-------|
|name|Name des Routers||
|route|Definiten des Routenverlaufs

Die einzelnen Routen werden wie folgt definiert

|Feld|Beschreibung|Default|
|----|------------|-------|
|type|Art des Routenpunktes (module, plugin, router)||
|name|Zu ladende Resource (vollständige Liste siehe !!!TBD!!!)||
|config|Konfigurationseinstellungen des Routenpunktes||

Bsp:
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
### Module
#### `filter.modeFilter`

|Feld|Beschreibung|Default|
|----|------------|-------|
|allowed|Liste der erlaubten Paket Typen (fms, zvei, pocsag)||

Bsp:
```yaml
config:
  allowed:
  - fms
  - zvei
```

---
### Plugins