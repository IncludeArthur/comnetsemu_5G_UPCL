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

    h1 = net.addDockerHost(
        "h1",
        dimage="free5gc_v2",
        ip="192.168.0.101",
        #dcmd="echo",
        docker_args={
            "hostname": "h1",
            "ports": {"5000/tcp":5000},
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
        },
    )

    info("*** Adding switch and links\n")

    info("\n*** Starting network\n")
    net.start()

    if not AUTOTEST_MODE:
        CLI(net)

    net.stop()
