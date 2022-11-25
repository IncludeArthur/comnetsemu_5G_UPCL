#!/usr/bin/env bash

LOG_PATH="/free5gc/log/"
LOG_NAME="free5gc.log"

# --- start upf ---

/free5gc/bin/upf -c /free5gc/config/upfcfg.yaml -l ${LOG_PATH}upf.log -lc ${LOG_PATH}${LOG_NAME} &
SUDO_UPF_PID=$!
sleep 0.1
UPF_PID=$(pgrep -P $SUDO_UPF_PID)
PID_LIST+=($SUDO_UPF_PID $UPF_PID)

