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

    prj_folder = "/home/ubuntu/comnetsemu_free5gc"
    mongodb_folder = "/home/ubuntu/mongodbdata"

    net = Containernet(controller=Controller, link=TCLink, xterms=False)

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Creating hosts\n")

    info("*** Add core network\n")

    cp = net.addDockerHost(
        "cp",
        dimage="free5gc",
        ip="192.168.0.101",
        #dcmd="/free5gc/scripts/run_core.sh",
        docker_args={
            "hostname": "cp",
            "ports": {"5000/tcp":5000,"8000" :8000},
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

    iupf = net.addDockerHost(
        "iupf",
        dimage="free5gc",
        ip="192.168.0.102",
        #dcmd="/free5gc/scripts/run_core.sh",
        docker_args={
            "hostname": "iupf",
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

    psaupf = net.addDockerHost(
        "psaupf",
        dimage="free5gc",
        ip="192.168.0.103",
        #dcmd="/free5gc/scripts/run_core.sh",
        docker_args={
            "hostname": "psaupf",
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

    # psaupf2 = net.addDockerHost(
    #     "psa-upf2",
    #     dimage="free5gc",
    #     ip="192.168.0.104",
    #     #dcmd="/free5gc/scripts/run_core.sh",
    #     docker_args={
    #         "hostname": "psa-upf2",
    #         "volumes": {
    #             prj_folder + "/free5gc/config":{
    #                 "bind": "/free5gc/config",
    #                 "mode": "rw",
    #             },
    #             prj_folder + "/free5gc/scripts":{
    #                 "bind": "/free5gc/scripts",
    #                 "mode": "rw",
    #             },
    #             prj_folder + "/log": {
    #                 "bind": "/free5gc/log",
    #                 "mode": "rw",
    #             },
    #             mongodb_folder :{
    #                 "bind": "/free5gc/mongodb",
    #                 "mode": "rw",
    #             },
    #         },
    #         "cap_add": ["NET_ADMIN"],
    #         "sysctls": {"net.ipv4.ip_forward": 1},
    #         "devices": "/dev/net/tun:/dev/net/tun:rwm"
    #     },
    # )


    info("*** Add gNB and UE\n")

    gnb = net.addDockerHost(
        "gnb",
        dimage="ueransim",
        ip="192.168.0.201",
        #dcmd="echo",
        docker_args={
            "hostname": "gnb",
            "volumes": {
                prj_folder + "/ueransim/config":{
                    "bind": "/UERANSIM/config",
                    "mode": "rw",
                },
                prj_folder + "/ueransim/scripts":{
                    "bind": "/UERANSIM/scripts",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/UERANSIM/log",
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
    net.addLink(cp,  s2, bw=1000, delay="1ms", intfName1="cp-s2",  intfName2="s2-cp")
    net.addLink(iupf,  s2, bw=1000, delay="1ms", intfName1="iupf-s2",  intfName2="s2-iupf")
    net.addLink(psaupf,  s2, bw=1000, delay="1ms", intfName1="psaupf-s2",  intfName2="s2-psaupf")
 
    info("\n*** Starting network\n")
    net.start()

    if not AUTOTEST_MODE:
        CLI(net)

    net.stop()
