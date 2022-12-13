#!/usr/bin/env bash

LOG_PATH="/free5gc/log/"
LOG_NAME="free5gc.log"

# --- start mongodb ---
mongod --dbpath /free5gc/mongodb --logpath /free5gc/log/mongodb.log --logRotate reopen --logappend --bind_ip_all &

sleep 5

# --- start webconsole ---
/free5gc/webconsole/bin/webconsole -c /free5gc/config/webuicfg.yaml -p /free5gc/webconsole/public -l ${LOG_PATH}webui.log -lc ${LOG_PATH}${LOG_NAME} &

sleep 1

# --- start upf ---

/free5gc/bin/upf -c /free5gc/config/upfcfg.yaml -l ${LOG_PATH}upf.log -lc ${LOG_PATH}${LOG_NAME} &

sleep 1

# --- start control plain functions ---

NF_LIST="nrf amf smf udr pcf udm nssf ausf"

#export GIN_MODE=release

for NF in ${NF_LIST}; do
    /free5gc/bin/${NF} -c /free5gc/config/${NF}cfg.yaml -l ${LOG_PATH}${NF}.log -lc ${LOG_PATH}${LOG_NAME} &
    sleep 0.1
done