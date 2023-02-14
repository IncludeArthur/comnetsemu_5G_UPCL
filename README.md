# Comnetsemu Free5GC ULCL

This project emulates a full 5G network and test the Uplink Classifier (ULCL) functionalities.

### Dependencies
- [Comnetsemu](https://git.comnets.net/public-repo/comnetsemu)
- [Free5GC](https://github.com/free5gc/free5gc)
- [UERANSIM](https://github.com/aligungr/UERANSIM)

### Network Topolgy
![ULCL](./figures/comnetsemu_ulcl_architecture.png)

### Environment setup

Install the latest version of Comnetsemu in a Ubuntu 20.04 VM following one of the 
[available options](https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs).

Inside the VM, download and install the [gtp5g kernel module](https://github.com/free5gc/gtp5g) required by the UPF.
```
git clone -b v0.6.8 https://github.com/free5gc/gtp5g.git
cd gtp5g
make
sudo make install
```
Clone this repository in the comnetsemu VM.

Build the Free5GC Docker image
```
cd free5gc
docker build --no-cache --force-rm -t free5gc .
```
Build the UERANSIM Docker image
```
cd ueransim
docker build --no-cache --force-rm -t ueransim .
```

Customize the following variables in the ```example_ulcl.py``` file
- ```prj_folder```: pointing at the local repository
- ```mongodb_folder```: pointing at a user-defined path where the MongoDB data will be stored

### Running the project

To start the network topology run

```$ sudo python3 example_ulcl.py```

The script creates the hosts and automatically start the 5GC, gNB and UE.

If it is the first time executing the script, the UE connection will fail since there are no subscribers registered in the database.
To fix the problem simply connect to the Free5GC webconsole from the Comnetsemu VM at the address
```
localhost:5000/
```
Using the default credentials
```
Username: admin
Password: free5gc
```

Navigate to the SUBSCRIBERS tab and press the New Subscriber button. 
Insert the missing data using the SUPI ```imsi-208930000000003``` and Submit.
![](https://camo.githubusercontent.com/71579c2bad8c44efc3311bcf9651e30293f28d232bb18a78c871d483a6ef2897/68747470733a2f2f692e696d6775722e636f6d2f614375524a745a2e706e67)

### Testing the functionalities

Enter the UE container
```
$ ./enter_container.sh ue
```
Verify the UE connectivity with a ping test on the uesimtun0 TUNnel interface
```
# ping -I uesimtun0 8.8.8.8
```
Confirm using tcpdump that the packet goes through the PSA-UPF1.
```
$ ./enter_container.sh psaupf1
$ tcpdump
```
Ping 172.17.0.1 and 172.18.0.1 and confirm that the packets go through the PSA-UPF1 and PSA-UPF2 respectively, accordingly to the uerouting.yaml configuration.
