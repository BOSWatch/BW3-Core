#!/usr/bin/python3
# -*- coding: utf-8 -*-
r"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        http.py
@date:        21.07.2025
@author:      Claus Schichl
@description: Install Service File with argparse CLI
"""

import os
import subprocess
import sys
import logging
import argparse
import yaml
from colorama import init as colorama_init, Fore, Style
from pathlib import Path

# === Initialisiere Colorama für Windows/Konsole ===
colorama_init(autoreset=True)

# === Konstanten ===
BASE_DIR = Path(__file__).resolve().parent
BW_DIR = '/opt/boswatch3'
SERVICE_DIR = Path('/etc/systemd/system')
CONFIG_DIR = (BASE_DIR / 'config').resolve()
LOG_FILE = (BASE_DIR / 'log' / 'install' / 'service_install.log').resolve()
os.makedirs(LOG_FILE.parent, exist_ok=True)

# === Sprache (kapselt globale Variable) ===
_lang = 'de'


def get_lang():
    return _lang


def set_lang(lang):
    global _lang
    _lang = lang


# === Texte ===
TEXT = {
    "de": {
        "script_title": "🛠️ BOSWatch Service Manager",
        "mode_dry": "DRY-RUN (nur Vorschau)",
        "mode_live": "LIVE",
        "no_yaml": "❌ Keine .yaml-Dateien im config-Verzeichnis gefunden.",
        "found_yaml": "🔍 Gefundene YAML-Dateien: {}",
        "action_prompt": "\nWas möchtest du tun? (i=installieren, r=entfernen, e=beenden): ",
        "edited_prompt": "Wurden die YAML-Dateien korrekt bearbeitet? (y/n): ",
        "edit_abort": "⚠️ Bitte YAML-Dateien zuerst bearbeiten. Vorgang abgebrochen.",
        "install_confirm": "Service für '{}' installieren? (y/n): ",
        "skip_invalid_yaml": "⏭ Überspringe fehlerhafte YAML: {}",
        "install_done": "✅ Installation abgeschlossen. Services installiert: {}, übersprungen: {}",
        "invalid_input": "Ungültige Eingabe. Erlaubt sind: {}",
        "no_services": "Keine bw3-Services gefunden.",
        "available_services": "\nVerfügbare bw3-Services:",
        "remove_prompt": "Was soll deinstalliert werden? ",
        "invalid_choice": "Ungültige Auswahl.",
        "not_root": "🛑 Dieses Skript muss mit Root-Rechten ausgeführt werden (sudo).",
        "help_dry_run": "Nur anzeigen, nicht ausführen",
        "help_verbose": "Ausführliche Ausgabe",
        "help_quiet": "Weniger Ausgabe",
        "help_lang": "Sprache für alle Ausgaben [de/en] (Standard: de)",
        "creating_service_file": "📄 Erstelle Service-Datei für {} → {}",
        "removing_service": "\n🗑 Entferne Service: {}",
        "service_deleted": "{} gelöscht.",
        "service_not_found": "{} nicht gefunden oder im Dry-Run-Modus.",
        "yaml_error": "⚠ Fehler in YAML {}: {}",
        "yaml_read_error": "⚠ Fehler beim Lesen der YAML-Datei {}: {}",
        "unknown_yaml_type": "⚠ YAML-Typ für {} nicht erkannt. Service wird übersprungen.",
        "verify_warn": "⚠ Warnung bei systemd-analyze verify:\n{}",
        "verify_ok": "{} erfolgreich verifiziert.",
        "install_skipped": "⏭ Installation für '{}' übersprungen",
        "file_write_error": "⚠ Fehler beim Schreiben der Datei {}: {}",
        "all": "[a] Alle deinstallieren",
        "exit": "[e] Beenden",
        "service_active": "✅ Service {0} läuft erfolgreich.",
        "service_inactive": "⚠  Service {0} ist **nicht aktiv** – bitte prüfen.",
        "dryrun_status_check": "🧪 [Dry-Run] Service-Status von {0} würde jetzt geprüft.",
        "max_attempts_exceeded": "❌ Maximale Anzahl an Eingabeversuchen überschritten. Das Menü wird beendet."

    },
    "en": {
        "script_title": "🛠️ BOSWatch Service Manager",
        "mode_dry": "DRY-RUN (preview only)",
        "mode_live": "LIVE",
        "no_yaml": "❌ No .yaml files found in config directory.",
        "found_yaml": "🔍 YAML files found: {}",
        "action_prompt": "\nWhat would you like to do? (i=install, r=remove, e=exit): ",
        "edited_prompt": "Have the YAML files been edited correctly? (y/n): ",
        "edit_abort": "⚠ Please edit the YAML files first. Aborting.",
        "install_confirm": "Install service for '{}' ? (y/n): ",
        "skip_invalid_yaml": "⏭ Skipping invalid YAML: {}",
        "install_done": "✅ Installation complete. Services installed: {}, skipped: {}",
        "invalid_input": "Invalid input. Allowed: {}",
        "no_services": "No bw3 services found.",
        "available_services": "\nAvailable bw3 services:",
        "remove_prompt": "What should be removed? ",
        "invalid_choice": "Invalid choice.",
        "not_root": "🛑 This script must be run as root (sudo).",
        "help_dry_run": "Show actions only, do not execute",
        "help_verbose": "Show detailed output",
        "help_quiet": "Reduce output verbosity",
        "help_lang": "Language for all output [de/en] (default: de)",
        "creating_service_file": "📄 Creating service file for {} → {}",
        "removing_service": "\n🗑 Removing service: {}",
        "service_deleted": "{} deleted.",
        "service_not_found": "{} not found or in dry-run mode.",
        "yaml_error": "⚠ YAML error in {}: {}",
        "yaml_read_error": "⚠ Error reading YAML file {}: {}",
        "unknown_yaml_type": "⚠ Unknown YAML type for {}. Skipping service.",
        "verify_warn": "⚠ Warning in systemd-analyze verify:\n{}",
        "verify_ok": "{} verified successfully.",
        "install_skipped": "⏭ Installation skipped for '{}'",
        "file_write_error": "⚠ Error writing file {}: {}",
        "all": "[a] Remove all",
        "exit": "[e] Exit",
        "service_active": "✅ Service {0} is running successfully.",
        "service_inactive": "⚠ Service {0} is **not active** – please check.",
        "dryrun_status_check": "🧪 [Dry-Run] Service status of {0} would be checked now.",
        "max_attempts_exceeded": "❌ Maximum number of input attempts exceeded. Exiting menu."
    }
}


# === Logging Setup ===
def setup_logging(verbose=False, quiet=False):
    """
    Setup logging to file and console with colorized output.
    """
    log_level = logging.INFO
    if quiet:
        log_level = logging.WARNING
    elif verbose:
        log_level = logging.DEBUG

    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File Handler (plain)
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console Handler (colorized)
    class ColorFormatter(logging.Formatter):
        COLORS = {
            logging.DEBUG: Fore.CYAN,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.RED + Style.BRIGHT,
        }

        def format(self, record):
            color = self.COLORS.get(record.levelno, Fore.RESET)
            message = super().format(record)
            return f"{color}{message}{Style.RESET_ALL}"

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(ColorFormatter('%(levelname)s: %(message)s'))
    logger.addHandler(ch)

    return logger


def t(key):
    """
    Translation helper: returns the localized string for the given key.
    """
    lang = get_lang()
    return TEXT.get(lang, TEXT['de']).get(key, key)


def get_user_input(prompt, valid_inputs, max_attempts=3):
    """
    Prompt user for input until a valid input from valid_inputs is entered or max_attempts exceeded.
    Raises RuntimeError on failure.
    """
    attempts = 0
    while attempts < max_attempts:
        value = input(prompt).strip().lower()
        if value in valid_inputs:
            return value
        logging.warning(t("invalid_input").format(", ".join(valid_inputs)))
        attempts += 1
    raise RuntimeError("Maximale Anzahl Eingabeversuche überschritten.")


def list_yaml_files():
    """
    Returns a list of .yaml or .yml files in the config directory.
    """
    return [f.name for f in CONFIG_DIR.glob("*.y*ml")]


def test_yaml_file(file_path):
    """
    Tests if YAML file can be loaded without error.
    """
    try:
        content = file_path.read_text()
        yaml.safe_load(content)
        return True
    except Exception as e:
        logging.error(t("yaml_error").format(file_path, e))
        return False


def detect_yaml_type(file_path):
    """
    Detects if YAML config is 'client' or 'server' type.
    """
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        if 'client' in data:
            return 'client'
        elif 'server' in data:
            return 'server'
        else:
            logging.error(t("unknown_yaml_type").format(os.path.basename(file_path)))
            return None
    except Exception as e:
        logging.error(t("yaml_read_error").format(file_path, e))
        return None


def execute(command, dry_run=False):
    """
    Executes shell command unless dry_run is True.
    """
    logging.debug(f"→ {command}")
    if not dry_run:
        subprocess.run(command, shell=True, check=False)


def verify_service(service_path):
    """
    Runs 'systemd-analyze verify' on the service file and logs warnings/errors.
    """
    try:
        result = subprocess.run(['systemd-analyze', 'verify', service_path], capture_output=True, text=True)
        if result.returncode != 0 or result.stderr:
            logging.warning(t("verify_warn").format(result.stderr.strip()))
        else:
            logging.debug(t("verify_ok").format(os.path.basename(service_path)))
    except Exception as e:
        logging.error(t("yaml_error").format(service_path, e))


def install_service(yaml_file, dry_run=False):
    """
    Creates and installs systemd service based on YAML config.
    """
    yaml_path = CONFIG_DIR / yaml_file
    yaml_type = detect_yaml_type(yaml_path)
    if yaml_type == 'server':
        is_server = True
    elif yaml_type == 'client':
        is_server = False
    else:
        logging.error(t("unknown_yaml_type").format(yaml_file))
        return

    service_name = f"bw3_{Path(yaml_file).stem}.service"
    service_path = SERVICE_DIR / service_name

    if is_server:
        exec_line = f"/usr/bin/python {BW_DIR}/bw_server.py -c {yaml_file}"
        description = "BOSWatch Server"
        after = "network-online.target"
        wants = "Wants=network-online.target"
    else:
        exec_line = f"/usr/bin/python3 {BW_DIR}/bw_client.py -c {yaml_file}"
        description = "BOSWatch Client"
        after = "network.target"
        wants = ""

    service_content = f"""[Unit]
Description={description}
After={after}
{wants}

[Service]
Type=simple
WorkingDirectory={BW_DIR}
ExecStart={exec_line}
Restart=on-abort

[Install]
WantedBy=multi-user.target
"""

    logging.info(t("creating_service_file").format(yaml_file, service_name))

    if not dry_run:
        try:
            with open(service_path, 'w') as f:
                f.write(service_content)
        except IOError as e:
            logging.error(t("file_write_error").format(service_path, e))
            return
        verify_service(service_path)

    execute("systemctl daemon-reexec", dry_run=dry_run)
    execute(f"systemctl enable {service_name}", dry_run=dry_run)
    execute(f"systemctl start {service_name}", dry_run=dry_run)
    if not dry_run:
        try:
            subprocess.run(
                ["systemctl", "is-active", "--quiet", service_name],
                check=True
            )
            logging.info(t("service_active").format(service_name))
        except subprocess.CalledProcessError:
            logging.warning(t("service_inactive").format(service_name))
    else:
        logging.info(t("dryrun_status_check").format(service_name))


def remove_service(service_name, dry_run=False):
    """
    Stops, disables and removes the given systemd service.
    """
    logging.warning(t("removing_service").format(service_name))
    execute(f"systemctl stop {service_name}", dry_run=dry_run)
    execute(f"systemctl disable {service_name}", dry_run=dry_run)
    service_path = Path(SERVICE_DIR) / service_name
    if not dry_run and service_path.exists():
        try:
            os.remove(service_path)
            logging.info(t("service_deleted").format(service_name))
        except Exception as e:
            logging.error(t("file_write_error").format(service_path, e))
    else:
        logging.warning(t("service_not_found").format(service_name))


def remove_menu(dry_run=False):
    """
    Interactive menu to remove services.
    """
    while True:
        services = sorted([
            f for f in os.listdir(SERVICE_DIR)
            if f.startswith('bw3_') and f.endswith('.service')
        ])

        if not services:
            print(Fore.YELLOW + t("no_services") + Style.RESET_ALL)
            return

        print(Fore.CYAN + "\n" + t("available_services") + Style.RESET_ALL)
        for i, s in enumerate(services):
            print(f" [{i}] {s}")
        print(" " + t("all"))
        print(" " + t("exit"))

        try:
            auswahl = get_user_input(
                t("remove_prompt"),
                ['e', 'a'] + [str(i) for i in range(len(services))]
            )
        except RuntimeError:
            logging.error(t("max_attempts_exceeded"))
            break

        if auswahl == 'e':
            break
        elif auswahl == 'a':
            for s in services:
                remove_service(s, dry_run=dry_run)
            # Danach direkt weiter zur nächsten Schleife (aktualisierte Liste!)
            continue
        else:
            remove_service(services[int(auswahl)], dry_run=dry_run)
            # Danach ebenfalls weiter zur nächsten Schleife (aktualisierte Liste!)
            continue


def init_language():
    """
    Parses --lang/-l argument early to set language before other parsing.
    """
    lang_parser = argparse.ArgumentParser(add_help=False)
    lang_parser.add_argument(
        '--lang', '-l',
        choices=['de', 'en'],
        default='de',
        metavar='LANG',
        help=TEXT["en"]["help_lang"]
    )
    lang_args, remaining_argv = lang_parser.parse_known_args()
    set_lang(lang_args.lang)
    return lang_parser, remaining_argv


def main(dry_run=False):
    """
    Hauptprogramm: Service installieren oder entfernen.
    """
    print(Fore.GREEN + Style.BRIGHT + t("script_title") + Style.RESET_ALL)
    print(t('mode_dry') if dry_run else t('mode_live'))
    print()

    yaml_files = list_yaml_files()
    if not yaml_files:
        print(Fore.RED + t("no_yaml") + Style.RESET_ALL)
        sys.exit(1)

    print(Fore.GREEN + t("found_yaml").format(len(yaml_files)) + Style.RESET_ALL)
    for f in yaml_files:
        file_path = CONFIG_DIR / f
        valid = test_yaml_file(file_path)
        status = Fore.GREEN + "✅" if valid else Fore.RED + "❌"
        print(f" - {f} {status}{Style.RESET_ALL}")

    try:
        action = get_user_input(t("action_prompt"), ['i', 'r', 'e'])
    except RuntimeError:
        logging.error("Maximale Anzahl Eingabeversuche überschritten. Beende Programm.")
        sys.exit(1)

    if action == 'e':
        sys.exit(0)
    elif action == 'r':
        remove_menu(dry_run=dry_run)
        return

    try:
        edited = get_user_input(t("edited_prompt"), ['y', 'n'])
    except RuntimeError:
        logging.error("Maximale Anzahl Eingabeversuche überschritten. Beende Programm.")
        sys.exit(1)

    if edited == 'n':
        print(Fore.YELLOW + t("edit_abort") + Style.RESET_ALL)
        sys.exit(0)

    installed = 0
    skipped = 0

    for yaml_file in yaml_files:
        file_path = CONFIG_DIR / yaml_file
        if not test_yaml_file(file_path):
            print(Fore.RED + t("skip_invalid_yaml").format(yaml_file) + Style.RESET_ALL)
            skipped += 1
            continue

        try:
            install = get_user_input(t("install_confirm").format(yaml_file), ['y', 'n'])
        except RuntimeError:
            logging.error("Maximale Anzahl Eingabeversuche überschritten. Überspringe Service.")
            skipped += 1
            continue

        if install == 'y':
            install_service(yaml_file, dry_run=dry_run)
            installed += 1
        else:
            logging.info(t("install_skipped").format(yaml_file))
            skipped += 1

    print()
    logging.info(t("install_done").format(installed, skipped))


if __name__ == "__main__":
    lang_parser, remaining_argv = init_language()

    parser = argparse.ArgumentParser(
        description=t("script_title"),
        parents=[lang_parser]
    )
    parser.add_argument('--dry-run', action='store_true', help=t("help_dry_run"))
    parser.add_argument('--verbose', action='store_true', help=t("help_verbose"))
    parser.add_argument('--quiet', action='store_true', help=t("help_quiet"))

    args = parser.parse_args(remaining_argv)

    setup_logging(verbose=args.verbose, quiet=args.quiet)

    if os.geteuid() != 0:
        print(Fore.RED + t("not_root") + Style.RESET_ALL)
        sys.exit(1)

    try:
        main(dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer.")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unbehandelter Fehler: {e}")
        sys.exit(1)
# === Ende des Skripts ===
