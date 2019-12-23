#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from pyzabbix import ZabbixAPI
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
import os

hostgrp_dictionary = { #hostgrp table on zabbix db
    "B2B AVANÇADOS": 15,
    "ABILITY_INTERIOR": 16,
    "ABILITY_CAPITAL": 17,
    "ICOMON_ABCD": 18,
    "ICOMON_AT": 19,
    "ICOMON_CENTRO": 20,
    "ICOMON_LESTE": 21,
    "ICOMON_VM": 22,
    "TEL_CAPITAL": 23,
    "TEL_INTERIOR": 24,
    "TEL_JI": 25,
    "TEL_LITORAL": 26,
    "TEL_PC_SC": 27,
    "TELEMONT": 28,
    "VIVO": 29,
    "Capital": 30,
    "Interior": 31
}

dictionary_2 = { #hosts table on zabbix db
    "CPE_B2B": 10308,
    "CPE_B2C": 10309
}

dictionary_3 = {
    "NRC": 1,
    "NRO_TELEFONE13": 2,
    "IP_FIXO": 3,
    "NOME_REDE_OLT": 4,
    "CONTRATO": 5,
    "DATA_CRIACAO_CLIENTE": 6,
    "GESTAO": 7
}


# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = 'https://201.28.110.3/zabbix'

zapi = ZabbixAPI(ZABBIX_SERVER)

# Disable SSL certificate verification
zapi.session.verify = False

zapi.login('Admin', 'zabbix')
for h in zapi.host.get():
    print(h['host'])

bar = ProgressBar(maxval=rows, widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()

i = 0

directory = os.fsencode('b2b_nagios/')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".cfg"):
        print(os.path.join(directory, filename))
    else:
        continue

print()