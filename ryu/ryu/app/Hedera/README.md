## Hedera

Hedera is a SDN-based traffic schduling application implementating "Hedera", see the paper "Hedera: dynamic flow scheduling for data center networks" by Mohammad Al-Fares. Initially, network traffic is routed with ECMP. Once the speed of any flow in the switch exceeds 10% of the bandwidth of the link, routing path will be calculated and installed by the Ryu controller to reschedule the flow to other light loading path.
It includes a set of Ryu applications collecting basic network information, such as topology and free bandwidth of links. Fortunately, our application supports load balancing based on dynamic traffic information.

The detailed information of the modules is shown below:

* Fattree4 and Fattree8 are topology modules;

* Network Awareness is the module for collecting network information;

* Network Monitor is the module for collecting traffic information;

* DemandEstimation is the module for estimating flow demand;

* Hedera is the main module of the application;

* Setting is the module including common setting.

We make use of networkx's data structure to store topology. Meanwhile, we also utilize networkx's built-in algorithm to calculate shortest paths.


### Prerequisites

The following softwares should have been installed in your machine.
* Mininet: git clone git://github.com/mininet/mininet; mininet/util/install.sh -a
* Ryu: git clone git://github.com/osrg/ryu.git; cd ryu; python3 -m pip install .
* Networkx: python3 -m pip install networkx


### Download

Download files into Ryu directory, for instance, 'ryu/ryu/app/Hedera' is OK.


### Make some change

To register parsing parameters, you NEED to add the following code into the end of ryu/ryu/flags.py.

    CONF.register_cli_opts([
        # k_shortest_forwarding
        cfg.IntOpt('k_paths', default=4, help='number of candidate paths of KSP.'),
        cfg.StrOpt('weight', default='bw', help='weight type of computing shortest path.'),
        cfg.IntOpt('fanout', default=4, help='switch fanout number.')])


### Reinstall Ryu

You must reinstall Ryu, so that you can run the new code. In the top directory of Ryu project:

    sudo python3 setup.py install


### Quickstart (Ubuntu 24.04 / Python 3)

- Clean up any previous Mininet/OVS state (host shell):
  - sudo mn -c
  - for br in $(sudo ovs-vsctl list-br); do sudo ovs-vsctl --if-exists del-br "$br"; done
  - for ns in $(ip netns list | awk '{print $1}'); do sudo ip netns del "$ns"; done
  - ip -o link show | awk -F': ' '/@/ {print $2}' | cut -d@ -f1 | xargs -r -n1 sudo ip link del
- Start controller (host shell, listen on 6633 to match fattree default):
  - cd ryu
  - python3 -m ryu.cmd.manager --ofp-tcp-listen-port 6633 --observe-links ryu/app/Hedera/Hedera.py --k_paths=4 --weight=hop --fanout=4
    - Use --weight=bw to enable Hedera scheduling; use --weight=hop for ECMP baseline.
- Start topology (separate host shell):
  - sudo -E python3 ryu/app/Hedera/fattree4.py
- Validate in the Mininet CLI:
  - pingall
  - iperf

Notes:
- Wait for "[GET NETWORK TOPOLOGY]" in the controller logs before running tests.
- Links default to 10 Mbit/s; setting.MAX_CAPACITY is 10000 (Kbit/s) accordingly.


### Start

Note: If your controller does not run on the same machine, change the controller IP/port passed to Ryu or modify fattree module defaults accordingly. The provided fattree defaults connect to 127.0.0.1:6633. If your Ryu listens on 6653, change the port in fattree4/8.py when calling createTopo or pass --ofp-tcp-listen-port 6633 to Ryu to match the default.

Firstly, start up the network. An example is shown below:

    $ sudo -E python3 ryu/ryu/app/Hedera/fattree4.py

And then, go into the top directory of Ryu, and run the application. You are suggested to add arguments when starting Ryu. An example is shown below:

    $ cd ryu
    $ ryu-manager --ofp-tcp-listen-port 6633 --observe-links ryu/app/Hedera/Hedera.py --k_paths=4 --weight=hop --fanout=4

or:

    $ ryu-manager --ofp-tcp-listen-port 6633 --observe-links ryu/app/Hedera/Hedera.py --k_paths=16 --weight=hop --fanout=8

NOTE: After these, we should wait for the network to complete the initiation for several seconds, because LLDP needs some time to discovery the network topology. We can't operate the network until 'Get network topology' is printed in the terminal of the Ryu controller, otherwise, some error will occur. It may be about 10 seconds for fattree4, and a little longer for fattree8.

After that, test the correctness of Hedera:

    mininet> pingall
    mininet> iperf

If you want to show the collected information, you can set the parameters in setting.py. Also, you can change the setting as you like, such as the discovery period and monitor period. After that, you can see the information shown in the terminal.


### Authors

Siyi Chen, Zeyu Ma, Sijia Qian
