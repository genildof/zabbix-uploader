#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from pyzabbix import ZabbixAPI
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import pandas as pd
import threading
	
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
    "NRC": 0,
    "NRO_TELEFONE13": 1,
    "IP_FIXO": 2,
    "NOME_REDE_OLT": 3,
    "CONTRATO": 4,
    "DATA_CRIACAO_CLIENTE": 5,
    "GESTAO": 6
}

#loads CSV file
data = pd.read_csv("./BasePlus_Sigres_19062019.csv")

def process(k):
	print (str(threading.current_thread().name) + " => " + str(k[dictionary_3["IP_FIXO"]]))
	try:

		# The hostname at which the Zabbix web interface is available
		ZABBIX_SERVER = 'https://201.28.110.3/zabbix'
		zapi = ZabbixAPI(ZABBIX_SERVER)

		# Disable SSL certificate verification
		zapi.session.verify = False
		zapi.login('Admin', 'zabbix')
		
		zapi.host.create(
			host= str(k[dictionary_3["NOME_REDE_OLT"]]) + "_" + str(k[dictionary_3["NRO_TELEFONE13"]]),
			name= str(k[dictionary_3["CONTRATO"]]) + "_" + str(k[dictionary_3["NRC"]]),
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
				"value": str(k[dictionary_3["NOME_REDE_OLT"]])
			}],
			groups=[{
				"groupid": hostgrp_dictionary[str(k[dictionary_3["CONTRATO"]])]
			}],
			templates=[{
				"templateid": dictionary_2["CPE_B2C"]
			}],
			description= "NRC: " + str(k[dictionary_3["NRC"]]) + "\n" + 
				"NRO_TELEFONE13: " + str(k[dictionary_3["NRO_TELEFONE13"]]) + "\n" +
				"IP: " + str(k[dictionary_3["IP_FIXO"]]) + "\n" + 
				"NOME_REDE_OLT: " + str(k[dictionary_3["NOME_REDE_OLT"]]) + "\n" +
				"CONTRATO: " + str(k[dictionary_3["CONTRATO"]]) + "\n" +
				"DATA_CRIACAO_CLIENTE: " + str(k[dictionary_3["DATA_CRIACAO_CLIENTE"]]) + "\n" +
				"GESTAO: " + str(k[dictionary_3["GESTAO"]]) + "\n\n\n_gf_"
		)
		zapi.logout()
		sleep(20)
	except:
		print (f"Exception when creating the host {str(k[dictionary_3['NOME_REDE_OLT']])} {str(k[dictionary_3['NRO_TELEFONE13']])}")
		print("-"*60)
		traceback.print_exc(file=sys.stdout)
		print("-"*60)

def main():
	with ThreadPoolExecutor(max_workers = 15) as executor:

		tuples = [tuple(x) for x in data.values]
		
		print(f"Tuples size: {len(tuples)}")
			
		sleep(2)
		executor.map(process, tuples)

if __name__ == '__main__':
	main()