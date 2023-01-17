#!/usr/bin/env bash

LOG_PATH="/free5gc/log/"
LOG_NAME="free5gc.log"

# --- start upf ---

/free5gc/bin/upf -c /free5gc/config/ULCL/psaupfcfg2.yaml -l ${LOG_PATH}psaupf2.log -lc ${LOG_PATH}${LOG_NAME} &

sleep 0.1
