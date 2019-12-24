#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from pyzabbix import ZabbixAPI
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
import traceback
import pandas as pd

hostgrp_dictionary = {
    "B2B AVANÇADOS": 15,
    "ABILITY_SJ": 16,
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
    "CPE_B2C": 10308,
    "CPE_B2B": 10309
}

dictionary_3 = {
    "INST_VOZ": 3,
    "INST_BL": 10,
    "MODELO_ROTEADOR": 12,
    "CONTRATO": 20,
    "CANG": 25,
    "CABO": 29,
    "FIBRA": 30,
    "NOME_CLIENTE": 35,
    "OLT": 28,
    "CIDADE": 41,
    "IP_FIXO": 42
}


# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = 'https://201.28.110.3/zabbix'
CSV_FILE = './Clientes_SJC_B2B.csv'
LOG_FILE = './uploader_log_file.log'

zapi = ZabbixAPI(ZABBIX_SERVER)

# Disable SSL certificate verification
zapi.session.verify = False

zapi.login('Admin', 'zabbix')
for h in zapi.host.get():
    print(h['host'])

data = pd.read_csv(CSV_FILE)  
rows = len(data.index)

print("\nLinhas: " + str(rows) +"\n")

bar = ProgressBar(maxval=rows, widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()

i = 0

for k in data.itertuples(): 

    try:
        zapi.host.create(
            host= str(k[dictionary_3["OLT"]]) + "_" + str(k[dictionary_3["INST_BL"]]),
            name= str(k[dictionary_3["CONTRATO"]]) + "_" + str(k[dictionary_3["INST_VOZ"]]),
	    status= 0, # 1 for Inactive
	    interfaces=[{
		"type": 1,
		"main": "1",
		"useip": 1,
		"ip": str(k[dictionary_3["IP_FIXO"]]),
		"dns": "",
		"port": 10050
	    }],
	    tags=[{
		"tag": "OLT",
		"value": str(k[dictionary_3["OLT"]])
	    }],
	    groups=[{
	        "groupid": hostgrp_dictionary[str(k[dictionary_3["CONTRATO"]])]
	    }],
	    templates=[{
		"templateid": dictionary_2["CPE_B2C"]
	    }],
	    description= "INST_VOZ: " + str(k[dictionary_3["INST_VOZ"]]) + "\n" + 
		"INST_BL: " + str(k[dictionary_3["INST_BL"]]) + "\n" +
		"IP_FIXO: " + str(k[dictionary_3["IP_FIXO"]]) + "\n" + 
		"OLT: " + str(k[dictionary_3["OLT"]]) + "\n" +
		"CABO: " + str(k[dictionary_3["CABO"]]) + "\n" +
		"CANG: " + str(k[dictionary_3["CANG"]]) + "\n" +
		"CONTRATO: " + str(k[dictionary_3["CONTRATO"]]) + "\n\n\n__genildo.ferreira@telefonica.com__"
	    )

    except Exception as e:
        print(f"Exception when creating the host {str(k[dictionary_3['OLT']])} {str(k[dictionary_3['INST_BL']])}")

        with open(LOG_FILE, 'a') as f:
            f.write("-"*80)
            f.write(f"\nException when creating the host {str(k[dictionary_3['OLT']])} {str(k[dictionary_3['INST_BL']])}")
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write("\n")

    finally:
        i += 1
        bar.update(i)

bar.finish
print()
