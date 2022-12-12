#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

if __name__ == "__main__":

    # Only used for auto-testing.
    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    prj_folder = "/home/ubuntu/comnetsemu_5G_UPCL"
    mongodb_folder = "/home/ubuntu/mongodbdata"

    net = Containernet(controller=Controller, link=TCLink, xterms=False)

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Creating hosts\n")

    info("*** Add core network\n")

    core = net.addDockerHost(
        "core",
        dimage="free5gc_3.0.5",
        ip="192.168.0.101",
        #dcmd="echo",
        docker_args={
            "hostname": "core",
            "ports": {"5000/tcp":5000, "8000" :8000},
            "volumes": {
                prj_folder + "/free5gc/config":{
                    "bind": "/free5gc/config",
                    "mode": "rw",
                },
                prj_folder + "/free5gc/scripts":{
                    "bind": "/free5gc/scripts",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/free5gc/log",
                    "mode": "rw",
                },
                mongodb_folder :{
                    "bind": "/free5gc/mongodb",
                    "mode": "rw",
                },
            },
            "cap_add": ["NET_ADMIN"],
            "sysctls": {"net.ipv4.ip_forward": 1},
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Add gNB and UE\n")

    gnb = net.addDockerHost(
        "gnb",
        dimage="ueransim",
        ip="192.168.0.102",
        #dcmd="echo",
        docker_args={
            "hostname": "gnb",
            "volumes": {
                prj_folder + "/ueransim/config":{
                    "bind": "/ueransim/config",
                    "mode": "rw",
                },
                prj_folder + "/ueransim/scripts":{
                    "bind": "/ueransim/scripts",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/ueransim/log",
                    "mode": "rw",
                },
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding switch\n")

    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")

    info("*** Adding links\n")

    net.addLink(gnb,  s1, bw=1000, delay="1ms", intfName1="gnb-s1",  intfName2="s1-gnb")
    net.addLink(s1,  s2, bw=1000, delay="10ms", intfName1="s1-s2",  intfName2="s2-s1")
    net.addLink(core,  s2, bw=1000, delay="1ms", intfName1="core-s2",  intfName2="s2-core")

    info("\n*** Starting network\n")
    net.start()

    if not AUTOTEST_MODE:
        CLI(net)

    net.stop()
