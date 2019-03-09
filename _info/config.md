## Konfiguration

Die Konfiguration von BOSWatch 3 ist im YAML Format abgelegt und wird nachfolgend beschrieben.
Immer wenn für eine Einstellung ein **Default** Wert angegeben ist, muss diese Einstellung nicht
zwingend eingetragen werden.


### Client
tbd

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