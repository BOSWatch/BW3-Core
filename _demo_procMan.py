#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll
"""

from boswatch.processManager import ProcessManager
import logging.config
logging.config.fileConfig("config/logger_client.ini")

dircmd = ProcessManager("dir", textMode=True)
dircmd.start(True)

line = dircmd.readline()
while line is not None:
    if line is not "":
        print(line)
    line = dircmd.readline()

dircmd.stop()

"""
19.09.2019 10:44:20,170 - processManager  [DEBUG   ] create process instance dir - textMode: True
19.09.2019 10:44:20,170 - processManager  [DEBUG   ] start new process: ['dir']
19.09.2019 10:44:20,173 - processManager  [DEBUG   ] process started with PID 17616
Datentr„ger in Laufwerk C: ist OS
Volumeseriennummer: ####-####
Verzeichnis von C:\Git\BOSWatch-Core
19.09.2019  10:44    <DIR>          .
19.09.2019  10:44    <DIR>          ..
11.01.2018  11:24    <DIR>          .cache
19.09.2019  10:39    <DIR>          .git
08.03.2019  09:00               665 .gitignore
19.09.2019  10:44    <DIR>          .idea
19.09.2019  10:40    <DIR>          boswatch
11.03.2019  08:45             4.368 bw_client.py
11.03.2019  08:46             3.993 bw_server.py
11.03.2019  08:33    <DIR>          config
08.03.2019  09:00            35.147 LICENSE
19.09.2019  09:43    <DIR>          log
08.03.2019  09:00    <DIR>          logo
11.03.2019  08:33    <DIR>          module
11.03.2019  08:37    <DIR>          plugin
08.03.2019  09:00               521 README.md
19.09.2019  10:44               794 _demo_procMan.py
08.03.2019  09:00    <DIR>          test
08.03.2019  09:00    <DIR>          _bin
05.03.2019  09:46    <DIR>          _docu
11.03.2019  08:33    <DIR>          _gen
11.03.2019  08:33    <DIR>          _info
01.03.2019  13:19    <DIR>          __pycache__
6 Datei(en),         45.488 Bytes
17 Verzeichnis(se), 317.487.964.160 Bytes frei
19.09.2019 10:44:20,182 - processManager  [DEBUG   ] stopping process: dir
19.09.2019 10:44:20,182 - processManager  [DEBUG   ] process not running: dir
19.09.2019 10:44:20,183 - processManager  [DEBUG   ] process dir returned 0
"""
