# BOSWatch – Dienstinstallation (Service Setup)

## 🇩🇪 BOSWatch als Dienst verwenden
Es wird vorausgesetzt, dass BOSWatch unter `/opt/boswatch3` installiert ist.  
Falls du einen anderen Installationspfad nutzt, müssen alle Pfadangaben in dieser Anleitung, im Skript sowie in den generierten Service-Dateien entsprechend angepasst werden.

Für jeden Dienst muss eine eigene `*.yaml`-Datei im Ordner `config/` vorhanden sein.  
Beim Ausführen des Skripts wirst du interaktiv gefragt, welche dieser YAML-Dateien installiert oder übersprungen werden sollen.

### Dienst installieren
Als Erstes wechseln wir ins BOSWatch Verzeichnis:

```bash
cd /opt/boswatch3
```

Das Installationsskript `install_service.py` wird anschließend mit Root-Rechten ausgeführt:
```bash
sudo /opt/boswatch3/venv/bin/python3 install_service.py
```
Es folgt ein interaktiver Ablauf, bei dem du gefragt wirst, welche YAML-Dateien installiert oder entfernt werden sollen.

### Zusätzliche Optionen (fortgeschrittene Anwender)
Das Skript bietet zusätzliche CLI-Optionen für mehr Kontrolle:

```bash
usage: install_service.py [-h] [--verbose] [--quiet]

Installiert oder entfernt systemd-Services für BOSWatch basierend auf YAML-Konfigurationsdateien.

optional arguments:
  -h, --help     zeigt diese Hilfe an
  --dry-run      für Entwickler: führt keine echten Änderungen aus (Simulation)
  --verbose      zeigt ausführliche Debug-Ausgaben
  --quiet        unterdrückt alle Ausgaben außer Warnungen und Fehlern
  -l, --lang [de|en]  Sprache für alle Ausgaben (Standard: de)
```

### Neustart nach Serviceinstallation
Nach Durchlaufen des Skripts boote dein System erneut durch, um den korrekten Startvorgang zu überprüfen:
```bash
sudo reboot
```

### Kontrolle, ob alles funktioniert hat
Um zu kontrollieren, ob alles ordnungsgemäß hochgefahren ist, kannst du die zwei Services mit folgenden Befehlen abfragen und die letzten Log-Einträge ansehen:

1. Client-Service
```bash
sudo systemctl status bw3_[clientname].service
```

Ersetze [clientname] mit dem Namen, den deine client.yaml hat (Standardmäßig: client)

Um das Log zu schließen, "q" drücken.

2. Server-Service
```bash
sudo systemctl status bw3_[servername].service
```

Ersetze [servername] mit dem Namen, den deine server.yaml hat (Standardmäßig: server)

Um das Log zu schließen, "q" drücken.

**Beide Outputs sollten so ähnlich beginnen:**
```text
bw3_client.service - BOSWatch Client
     Loaded: loaded (/etc/systemd/system/bw3_client.service; enabled; preset: enabled)
     Active: active (running) since Mon 1971-01-01 01:01:01 CEST; 15min 53s ago
```

Falls du in deinen letzten Logzeilen keine Error vorfinden kannst, die auf einen Stopp des Clients bzw. Server hinweisen, läuft das Programm wie gewünscht, sobald du deinen Rechner startest.

### Logdatei
Alle Aktionen des Installationsskripts werden in der Datei log/install/service_install.log protokolliert.

### Hinweis
Nach der Installation oder Entfernung wird systemctl daemon-reexec automatisch aufgerufen, damit systemd die neuen oder entfernten Units korrekt verarbeitet.

---

## 🇬🇧 Use BOSWatch as a Service

We assume that BOSWatch is installed to `/opt/boswatch3`.  
If you are using a different path, please adjust all paths in this guide, in the script and in the generated service files accordingly.

Each service requires its own `*.yaml` file inside the `config/` folder.  
The script will interactively ask which YAML files to install or skip.

### Install the Service

First, change directory to BOSWatch folder:

```bash
cd /opt/boswatch3
```

After that, run the install script `install_service.py` with root permissions:

```bash
sudo /opt/boswatch3/venv/bin/python3 install_service.py -l en 
```

You will be guided through an interactive selection to install or remove desired services.

### Additional Options

The script supports additional CLI arguments for advanced usage:

```bash
usage: install_service.py [-h] [--dry-run] [--verbose] [--quiet]

Installs or removes BOSWatch systemd services based on YAML config files.

optional arguments:
  -h, --help     show this help message and exit
  --dry-run      simulate actions without making real changes
  --verbose      show detailed debug output
  --quiet        suppress all output except warnings and errors
  -l, --lang [de|en]  Language for all output (default: de)
```

### Reboot After Setup
After running the script, reboot your system to verify that the services start correctly:
```bash
sudo reboot
```

### Verifying Successful Setup
To check if everything started properly, you can query the two services and inspect the most recent log entries:

1. Client Service
```bash
sudo systemctl status bw3_[clientname].service
```

Replace [clientname] with the name of your client.yaml file (default: client).

To close the log, press "q".

2. Server Service
```bash
sudo systemctl status bw3_[servername].service
```

Replace [servername] with the name of your server.yaml file (default: server).

To close the log, press "q".

**Both outputs should start similarly to this:**
```text
bw3_client.service - BOSWatch Client
     Loaded: loaded (/etc/systemd/system/bw3_client.service; enabled; preset: enabled)
     Active: active (running) since Mon 1971-01-01 01:01:01 CEST; 15min 53s ago
```

If the latest log entries do not show any errors indicating a client or server crash, then the services are running correctly and will automatically start on boot.

### Log File

All actions of the installation script are logged to `log/install/service_install.log`.

### Note

After installation or removal, `systemctl daemon-reexec` is automatically triggered to reload unit files properly.
