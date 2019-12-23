#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from pyzabbix import ZabbixAPI
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
import pandas as pd
import socket

dictionary_3 = {
    "NRC": 1,
    "NRO_TELEFONE13": 2,
    "IP_FIXO": 3,
    "NOME_REDE_OLT": 4,
    "CONTRATO": 5,
    "DATA_CRIACAO_CLIENTE": 6,
    "GESTAO": 7
}

data = pd.read_csv("./BasePlus_Sigres_19062019.csv")  
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
