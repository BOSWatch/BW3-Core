#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll
"""

import yaml
import pprint
pp = pprint.PrettyPrinter(indent=4)

with open('config/client.yaml') as f:
    # use safe_load instead load
    dataMap = yaml.safe_load(f)

pp.pprint(dataMap)


#print(dataMap["decoder"]["fms"])

for server in dataMap["server"]:
    print(server["ip"])

