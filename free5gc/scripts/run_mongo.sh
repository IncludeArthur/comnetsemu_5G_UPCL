#!/usr/bin/env bash

mongod --dbpath /free5gc/mongodb --logpath /free5gc/log/mongodb.log --logRotate reopen --logappend --bind_ip_all &
