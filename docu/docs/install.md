# 🇩🇪 Anleitung zur Installation von BOSWatch3
Die Installation von BOSWatch3 wird mittels diesem bash-Skript weitestgehend automatisiert durchgeführt.
## 1. Installationsskript herunterladen
Zunächst wird das aktuelle Installationsskript heruntergeladen
Öffne ein Terminal und führe folgenden Befehl aus:

```bash
wget https://github.com/BOSWatch/BW3-Core/raw/master/install.sh
```

## 2. Installationsskript ausführen
Im Anschluss wird das Skript mit dem Kommando

```bash
sudo bash install.sh
```

ausgeführt.

### 2a. Optionale Parameter beim Installieren
Standardmäßig wird das Programm nach /opt/boswatch3 installiert. Folgende Parameter stehen zur Installation zur Verfügung:

| Parameter        | Zulässige Werte         | Beschreibung                                                                                        |
| ---------------- | ----------------------- | --------------------------------------------------------------------------------------------------- |
| `-r`, `--reboot` | *(kein Wert notwendig)* | Führt nach der Installation automatisch einen Neustart durch. Ohne Angabe erfolgt **kein** Reboot.  |
| `-b`, `--branch` | `master`, `develop`     | Wählt den zu installierenden Branch. `master` ist stabil (empfohlen), `develop` ist für Entwickler. |
| `-p`, `--path`   | z. B. `/opt/boswatch3`  | Installiert BOSWatch3 in ein anderes Verzeichnis (**nicht empfohlen**). Standard ist `/opt/boswatch3`.  |

**ACHTUNG:**
Eine Installation von BOSWatch3 in ein anderes Verzeichnis erfordert viele Anpassungen in den Skripten und erhöht das Risiko, dass das Programm zu Fehlern führt. Es wird dazu geraten, das Standardverzeichnis zu benutzen.

Falls eine Installation mit Parameter gewünscht wird, so kann dies wie in folgendem Beispiel gestartet werden:

```bash
sudo bash install.sh --branch master --path /opt/boswatch3 --reboot
```

## 3. Konfiguration nach der Installation
Nach der Installation muss die Konfiguration der Dateien `/opt/boswatch3/config/client.yaml`
und `/opt/boswatch3/config/server.yaml` angepasst werden (z.B. mit nano, WinSCP,...):

```bash
sudo nano /opt/boswatch3/config/client.yaml
```

und

```bash
sudo nano /opt/boswatch3/config/server.yaml
```

Passe die Einstellungen nach deinen Anforderungen an. Bei einem Upgrade einer bestehenden Version kann dieser Schritt ggf. entfallen.

**INFORMATION:**
Weitere Informationen zur Konfiguration:
[Konfiguration](/docu/docs/config.md)

## 4. Neustart
**WICHTIG:**
Bitte starte das System neu, bevor du BOSWatch3 zum ersten Mal startest!

```bash
sudo reboot
```

## 5. Start von BOSWatch3
weiter gehts bei [BOSWatch benutzen](usage.md)

---

# 🇬🇧 BOSWatch3 Installation Guide
The installation of BOSWatch3 is largely automated using this bash script.

## 1. Download the Installation Script
First, download the latest installation script.
Open a terminal and run the following command:

```bash
wget https://github.com/BOSWatch/BW3-Core/raw/master/install.sh
```

## 2. Run the Installation Script
Then run the script with the command:

```bash
sudo bash install.sh
```

### 2a. Optional Parameters for Installation
By default, the program is installed to `/opt/boswatch3`. The following parameters are available for installation:

| Parameter        | Allowed Values          | Description                                                                                           |
| ---------------- | -----------------------| --------------------------------------------------------------------------------------------------- |
| `-r`, `--reboot` | *(no value needed)*     | Automatically reboots the system after installation. Without this, **no** reboot will be performed.  |
| `-b`, `--branch` | `master`, `develop`     | Selects the branch to install. `master` is stable (recommended), `develop` is for developers.       |
| `-p`, `--path`   | e.g. `/opt/boswatch3`   | Installs BOSWatch3 to a different directory (**not recommended**). Default is `/opt/boswatch3`.     |

**WARNING:**  
Installing BOSWatch3 to a different directory requires many adjustments in the scripts and increases the risk of errors. It is recommended to use the default directory.

If you want to install with parameters, you can run the following example command:

```bash
sudo bash install.sh --branch master --path /opt/boswatch3 --reboot
```

## 3. Configuration After Installation
After installation, the configuration files `/opt/boswatch3/config/client.yaml`  
and `/opt/boswatch3/config/server.yaml` must be adjusted (e.g. using nano, WinSCP, ...):

```bash
sudo nano /opt/boswatch3/config/client.yaml
```

and

```bash
sudo nano /opt/boswatch3/config/server.yaml
```

Adjust the settings according to your requirements. If upgrading from an existing version, this step might be skipped.

**INFORMATION:**  
More information about configuration:  
[Configuration](/docu/docs/config.md)

## 4. Reboot
**IMPORTANT:**  
Please reboot the system before starting BOSWatch3 for the first time!

```bash
sudo reboot
```

## 5. Starting BOSWatch3
Continue with [Using BOSWatch](usage.md)