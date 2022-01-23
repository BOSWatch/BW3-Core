#!/bin/bash
# -*- coding: utf-8 -*-
"""
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __  / __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll
@file:        install.sh
@date:        14.04.2020
@author:      Bastian Schroll, Smeti
@description: Installation File for BOSWatch3
"""

"""
Die Installation von BOSWatch3 wird mittels diesem bash-Skript weitestgehend automatisiert durchgeführt.
Zunächst wird das aktuelle Installationsskript heruntergeladen:
wget https://github.com/BOSWatch/BW3-Core/raw/master/install.sh
Im Anschluss wird das Skript mit dem Kommando
sudo bash install.sh
ausgeführt.
Standardmäßig wird das Programm nach /opt/boswatch3 installiert. Folgende Parameter stehen zur Installation zur Verfügung:
Parameter 	zulässige Werte 	Funktion
-r / --reboot 	- 	Reboot nach Installation (Ohne Angabe: Kein Reboot)
-b / --branch 	dev 	Installiert einen anderen Branch (dev nicht empfohlen!)
-p / --path 	/your/path 	Installiert in ein anderes Verzeichnis (nicht empfohlen!)
    master ist der stabile, zur allgemeinen Nutzung vorgesehene Branch
    develop ist der aktuelle Entwicklungs-Branch (Nur für Entwickler empfohlen)
"""


function exitcodefunction {
  errorcode=$1
  action=$2
  module=$3

  if [ $errorcode -ne "0" ]; then
    echo "Action: ${action} on ${module} failed." >> ${boswatch_install_path}/setup_log.txt
    echo "Exitcode: ${errorcode}" >> ${boswatch_install_path}/setup_log.txt
    echo ""
    echo "Action: ${action} on ${module} failed."
    echo "Exitcode: ${errorcode}"
    echo ""
    echo " -> If you want to open an issue at https://github.com/BOSWatch/BW3-Core/issues"
    echo "    please post the logfile, located at ${boswatch_install_path}/setup_log.txt"
    exit 1
  else
    echo "Action: ${action} on ${module} ok." >> ${boswatch_install_path}/setup_log.txt
  fi
 }

tput clear
tput civis
echo "    ____  ____  ______       __      __       __       _____ "
echo "   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  / "
echo "  / __  / / / /\__ \| | /| / / __  / __/ ___/ __ \     /_ <  "
echo " / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /  "
echo "/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/   "
echo "                German BOS Information Script                "             
echo "                     by Bastian Schroll                      "
echo ""



# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root!" 1>&2
   exit 1
fi

echo "This may take several minutes... Don't panic!"
echo ""
echo "Caution, script does not install a webserver with PHP and MySQL"
echo "So you have to make up manually if you want to use MySQL support"

boswatchpath=/opt/boswatch3
boswatch_install_path=/opt/boswatch3_install
reboot=false

for (( i=1; i<=$#; i=$i+2 )); do
    t=$((i + 1))
    eval arg=\$$i
    eval arg2=\$$t

    case ${arg} in
      -r|--reboot) reboot=true ;;

      -b|--branch)
      case ${arg2} in
        dev|develop)  echo "       !!! WARNING: you are using the DEV BRANCH !!!       "; branch=dev ;;
        *) branch=master ;;
      esac ;;

      -p|--path)    echo " !!! WARNING: you'll install BOSWATCH to alternative path !!! "; boswatchpath=$arg2 ;;

      *) echo "Internal error!" ; exit 1 ;;
    esac
done

mkdir -p ${boswatchpath} ${boswatch_install_path}

echo ""

tput cup 13 15
echo "[ 1/9] [#--------]"
tput cup 15 5
echo "-> make an apt-get update................"
apt-get update -y > ${boswatch_install_path}/setup_log.txt 2>&1

tput cup 13 15
echo "[ 2/9] [##-------]"
tput cup 15 5
echo "-> download GIT and other stuff.........."
apt-get -y install git cmake build-essential libusb-1.0 qt5-qmake libpulse-dev libx11-dev sox >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? download stuff

tput cup 13 15
echo "[ 3/9] [###------]"
tput cup 15 5
echo "-> download Python, Yaml and other stuff.."
sudo apt-get -y install python3 python3-yaml python3-pip alsa-utils>> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? download python

tput cup 13 15
echo "[ 4/9] [####-----]"
tput cup 15 5
echo "-> download rtl_fm........................."
cd ${boswatch_install_path}
git clone --branch master https://github.com/osmocom/rtl-sdr.git rtl-sdr >> ${boswatch_install_path}/setup_log.txt 2>&1
cd ${boswatch_install_path}/rtl-sdr/
git checkout 2659e2df31e592d74d6dd264a4f5ce242c6369c8
exitcodefunction $? git-clone rtl-sdr

tput cup 13 15
echo "[ 5/9] [#####----]"
tput cup 15 5
echo "-> compile rtl_fm......................"
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? cmake rtl-sdr

make >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? make rtl-sdr

make install >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? make-install rtl-sdr

ldconfig >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? ldconfig rtl-sdr

tput cup 13 15
echo "[ 6/9] [######---]"
tput cup 15 5
echo "-> download multimon-ng................"
cd ${boswatch_install_path}
git clone --branch 1.1.8 https://github.com/EliasOenal/multimon-ng.git multimonNG >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? git-clone multimonNG

cd ${boswatch_install_path}/multimonNG/

tput cup 13 15
echo "[ 7/9] [#######--]"
tput cup 15 5
echo "-> compile multimon-ng................."
mkdir -p build
cd build
# Export environment variable for qt5
export QT_SELECT=qt5
qmake ../multimon-ng.pro >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? qmake multimonNG

make >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? make multimonNG

make install >> ${boswatch_install_path}/setup_log.txt 2>&1
exitcodefunction $? qmakeinstall multimonNG

tput cup 13 15
echo "[ 8/9] [########-]"
tput cup 15 5
echo "-> download BOSWatch3.................."

case ${branch} in
  "dev") git clone -b develop https://github.com/BOSWatch/BW3-Core ${boswatchpath} >> ${boswatch_install_path}/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BW3-Core-develop ;;
  *) git clone -b master https://github.com/BOSWatch/BW3-Core ${boswatchpath} >> ${boswatch_install_path}/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BW3-Core ;;
esac

tput cup 13 15
echo "[9/9] [#########]"
tput cup 15 5
echo "-> configure..........................."
cd ${boswatchpath}/
chmod +x *
echo $'# BOSWatch3 - blacklist the DVB drivers to avoid conflicts with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core' >> /etc/modprobe.d/boswatch_blacklist_sdr.conf

tput cup 17 1
tput rev # Schrift zur besseren lesbarkeit Revers
echo "BOSWatch is now installed in ${boswatchpath}/   Installation ready!"
tput sgr0 # Schrift wieder Normal
tput cup 19 3
echo "Watch out: to run BOSWatch3 you have to modify the server.yaml and client.yaml!"
echo "Do the following step to do so:"
echo "sudo nano ${boswatchpath}/config/client.yaml   eg. server.yaml"
echo "and modify the config as you need. This step is optional if you are upgrading an old version of BOSWatch3."
echo "You can read the instructions on https://docs.boswatch.de/"
tput setaf 1 # Rote Schrift
echo "Please REBOOT before the first start"
tput setaf 9 # Schrift zurücksetzen
echo "start Boswatch3 with"
echo "sudo python3 bw_client.py -c client.yaml   and    sudo python3 bw_server.py -c server.yaml"

tput cnorm

# cleanup
mkdir ${boswatchpath}/log/install -p
mv ${boswatch_install_path}/setup_log.txt ${boswatchpath}/log/install/
rm ${boswatch_install_path} -R

if [ $reboot = "true" ]; then
  /sbin/reboot
fi
