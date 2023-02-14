#!/usr/bin/env bash

LOG_PATH="/free5gc/log/"
LOG_NAME="free5gc.log"

# --- start upf ---

/free5gc/bin/upf -c /free5gc/config/ULCL/psaupfcfg1.yaml -l ${LOG_PATH}psaupf1.log -lc ${LOG_PATH}${LOG_NAME} &

sleep 0.5

sysctl -w net.ipv4.ip_forward=1
iptables -I INPUT --source 10.60.0.0/16 -j ACCEPT
iptables -t nat -I POSTROUTING --out-interface eth0 -j MASQUERADE
iptables -I FORWARD --in-interface eth0 --out-interface upfgtp -j ACCEPT
iptables -I FORWARD --in-interface oupfgtp --out-interface eth0 -j ACCEPT