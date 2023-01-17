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
        #dcmd="bash /free5gc/scripts/ULCL/run_iupf.sh",
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

    psaupf1 = net.addDockerHost(
        "psaupf1",
        dimage="free5gc",
        ip="192.168.0.103",
        #dcmd="bash /free5gc/scripts/ULCL/run_psaupf.sh",
        docker_args={
            "hostname": "psaupf1",
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

    psaupf2 = net.addDockerHost(
        "psaupf2",
        dimage="free5gc",
        ip="192.168.0.104",
        #dcmd="/free5gc/scripts/run_core.sh",
        docker_args={
            "hostname": "psaupf2",
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

    ue = net.addDockerHost(
        "ue",
        dimage="ueransim",
        ip="192.168.0.202",
        #dcmd="echo",
        docker_args={
            "hostname": "ue",
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
    s3 = net.addSwitch("s3")

    info("*** Adding links\n")

    net.addLink(s1,  s2, bw=1000, delay="10ms", intfName1="s1-s2",  intfName2="s2-s1")
    net.addLink(s2,  s3, bw=1000, delay="10ms", intfName1="s2-s3",  intfName2="s3-s2")

    net.addLink(ue,  s1, bw=1000, delay="1ms", intfName1="ue-s1",  intfName2="s1-ue")
    net.addLink(gnb,  s1, bw=1000, delay="1ms", intfName1="gnb-s1",  intfName2="s1-gnb")

    net.addLink(cp,  s2, bw=1000, delay="1ms", intfName1="cp-s2",  intfName2="s2-cp")
    net.addLink(iupf,  s2, bw=1000, delay="1ms", intfName1="iupf-s2",  intfName2="s2-iupf")

    net.addLink(psaupf1,  s3, bw=1000, delay="1ms", intfName1="psaupf1-s3",  intfName2="s3-psaupf1")
    net.addLink(psaupf2,  s3, bw=1000, delay="1ms", intfName1="psaupf2-s3",  intfName2="s3-psaupf2")
 
    info("\n*** Starting network\n")
    net.start()

    info("\n*** Executing initial cmds\n")

    iupf.cmd("bash /free5gc/scripts/ULCL/run_iupf.sh")
    psaupf1.cmd("bash /free5gc/scripts/ULCL/run_psaupf1.sh")
    psaupf2.cmd("bash /free5gc/scripts/ULCL/run_psaupf2.sh")
    cp.cmd("bash /free5gc/scripts/ULCL/run_cp.sh")

    gnb.cmd("/UERANSIM/build/nr-gnb -c ../config/free5gc-gnb.yaml &")
    ue.cmd("/UERANSIM/build/nr-ue -c ../config/free5gc-ue.yaml &")

    if not AUTOTEST_MODE:
        CLI(net)

    net.stop()