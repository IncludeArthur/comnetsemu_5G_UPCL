#!/usr/bin/env bash

LOG_PATH="/free5gc/log/"
LOG_NAME="free5gc.log"

# --- start upf ---

/free5gc/bin/upf -c /free5gc/config/ULCL/iupfcfg.yaml -l ${LOG_PATH}iupf.log -lc ${LOG_PATH}${LOG_NAME} &

