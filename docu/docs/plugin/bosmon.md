# <center>Bosmon</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, die empfangenen Daten an Bosmon weiter zu leiten.

## Unterstütze Alarmtypen
- Fms ***untested***
- Pocsag
- Zvei ***untested***

## Resource
`Bosmon Webserver & Networkchannel`

## Konfiguration
|Feld|Beschreibung|Default|
|----|------------|-------|
|fms|Zugangsdaten, um sich mit der Bosmon Instanz zu verbinden||
|pocsag|Zugangsdaten, um sich mit der Bosmon Instanz zu verbinden||
|zvei|Zugangsdaten, um sich mit der Bosmon Instanz zu verbinden||

**Beispiel:**
```yaml
  - type: plugin
	name: Bosmon Plugin
	res: bosmon
	config:
		hostname: "IP Oder Hostname"
		port: "8080"
		user: "test" 
		passwd: "123"
		channel: "channelname"
      
```

---
## Hilfreiche Anleitungen seitens Bosmon

|  https://www.bosmon.de/forum/viewtopic.php?p=21099#p21099| Anleitung zur Verbindung mit Bosmon |
|--|--|
|  |  |


---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- requests
- basicauth
