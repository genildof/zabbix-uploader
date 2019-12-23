#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from pyzabbix import ZabbixAPI
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
import pandas as pd
import socket

dictionary_3 = {
    "INST_VOZ": 9,
    "INST_BL": 10,
    "IP_FIXO": 3,
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

data = pd.read_csv("./Clientes_SJC_B2B.csv")  
rows = len(data.index)

print("\nLinhas: " + str(rows) +"\n")

i = 0

for k in data.itertuples():
	try:
		socket.inet_aton(k[dictionary_3["IP_FIXO"]])
	except socket.error:
		print("Invalid IP at line " + str(i) + " - " + k[dictionary_3["IP_FIXO"]] + " _ " + str(k[dictionary_3["NRO_TELEFONE13"]]))
	
	i += 1

print()
