#!/bin/bash

NF_LIST="nrf amf smf udr pcf udm nssf ausf n3iwf upf"

for NF in ${NF_LIST}; do
    pkill -9 /free5gc/bin/${NF}
done

killall tcpdump
ip link del upfgtp
ip link del ipsec0
ip link del xfrmi-default
rm /dev/mqueue/*
rm -f /tmp/free5gc_unix_sock
mongo --eval "db.NfProfile.drop()" free5gc
