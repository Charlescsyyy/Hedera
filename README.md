# Hedera

Hedera is an SDN-based traffic scheduling application that reproduces and slightly extends the ideas from **“Hedera: Dynamic Flow Scheduling for Data Center Networks”** (Mohammad Al-Fares et al.). Traffic is initially routed with ECMP. When a flow’s rate exceeds a threshold (e.g., ~10% of the link bandwidth), the Ryu controller computes an alternate path and installs new rules to move that flow onto a lighter-loaded path. The controller continuously collects topology and link-utilization information to support demand-aware load balancing.

---

## Modules

- **Fattree4** and **Fattree8** — topology generators (fat-tree with fanout 4 or 8).
- **Network Awareness** — collects basic network information (topology, link attributes).
- **Network Monitor** — samples per-link bandwidth utilization.
- **DemandEstimation** — estimates per-flow demand from measurements.
- **Hedera (main)** — core logic for dynamic flow scheduling.
- **Setting** — common configuration (intervals, thresholds, logging).


## Prerequisites

Before getting started with the project, ensure the following prerequisites are set up:

1. **Prepare your Ubuntu environment:**
   - Use a local Ubuntu machine or a Linux server as the working environment.

2. **Install Mininet:**
   - Clone Mininet from the official repository and run the installation script:
     ```bash
     git clone git://github.com/mininet/mininet
     sudo mininet/util/install.sh -a
     ```
   - This command will clone the Mininet repository and install Mininet with all necessary dependencies.

3. **Install Ryu:**
   - Clone the Ryu repository and install it using the following commands:
     ```bash
     git clone git://github.com/osrg/ryu.git
     cd ryu
     pip install .
     ```
   - These commands will clone the Ryu repository and install it via `pip`.

By following the steps above, you will have Mininet and Ryu successfully installed and ready to work on the project.

## Start

1) **Start the Mininet topology** (example for fat-tree k=4):

```bash
sudo python ryu/ryu/app/Hedera/fattree4.py
```

2) **Launch the controller** (from the top of your Ryu repo):

```bash
cd ryu
ryu-manager --observe-links ryu/app/Hedera/Hedera.py --k_paths=4 --weight=hop --fanout=4
```

Wait for topology discovery.

3) **Sanity Tests** in the Mininet CLI:

To ensure that the network environment is set up correctly and functioning as expected, conduct basic sanity tests in the Mininet CLI with the following commands:

- **Test network connectivity**:
  ```bash
  mininet> pingall

  mininet> h1 iperf -s
  mininet> h2 iperf -c h1

You can toggle printed metrics and adjust timers in `setting.py`:

- Discovery period (LLDP)
- Monitor period (bandwidth sampling)
- ECMP vs. Hedera scheduling thresholds
- Logging verbosity

Changes take effect on the next controller start.

---
