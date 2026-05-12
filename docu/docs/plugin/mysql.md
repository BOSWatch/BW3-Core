# <center>Mysql</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, die Alarmierungen in einer Mysql / Mariadb Datenbank zu speichern.
Das Plugin legt die Tabelle "boswatch" selbststaendig an, wenn diese nicht vorhanden ist.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`mysql`

## Konfiguration
|Feld|Beschreibung|Default|
|----|------------|-------|
|host|IP-Adresse bzw. URL des Hosts||
|user|Username||
|password|Passwort||
|database|Name der Datenbank||

**Beispiel:**
```yaml
  - type: plugin
    name: mysql
    res: mysql
    config:
      host: HOST
      user: USERNAME
      password: PASSWORD
      database: DATABASE
```

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- mysql-connector-python
