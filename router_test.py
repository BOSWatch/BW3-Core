#!/usr/bin/python
# -*- coding: utf-8 -*-

from boswatch.configYaml import ConfigYAML
from boswatch.packet import Packet
from boswatch.router import RouterManager

config = ConfigYAML()
config.loadConfigFile("config/server.yaml")

bwPack = Packet("{'timestamp': 1551421020.9004176, 'mode': 'zvei', 'zvei': '12345'}")

print()

routMan = RouterManager()

routMan.buildRouter(config)

print()
routMan.runRouter(config.get("alarmRouter"), bwPack)

print()
routMan.runRouter("Router 2", bwPack)


print()
exit()
