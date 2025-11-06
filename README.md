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

We use `networkx` for graph storage and shortest-path computation.

---


## Prerequisites

This repository already includes vendored copies of **Mininet** and **Ryu** under.

And **Networkx** should have been installed in your machine.
  ```bash
  pip install networkx
  ```

---

## Download

Download files into Ryu directory. eg. 'ryu/ryu/app/Hedera'.

---

## Reinstall Ryu

You must reinstall Ryu to run the new code. In the top directory of Ryu project:

```bash
cd ryu
sudo python setup.py install
```

---

## Start

Update the controller IP used by the topology launcher from the placeholder `192.168.56.101` to your machine’s `eth0` (or primary NIC) IP.  
Check with `ifconfig` / `ip addr`. If you skip this step, switches will fail to connect.

1) **Start the Mininet topology** (example for fat-tree k=4):

```bash
sudo python ryu/ryu/app/Hedera/fattree4.py
```

2) **Launch the controller** (from the top of your Ryu repo):

```bash
cd ryu
ryu-manager --observe-links ryu/app/Hedera/Hedera.py --k_paths=4 --weight=hop --fanout=4
```

Or for a larger topology:

```bash
ryu-manager --observe-links ryu/app/Hedera/Hedera.py --k_paths=16 --weight=hop --fanout=8
```

Wait for topology discovery. LLDP needs a few seconds to finish. Don’t interact until you see `Get network topology` in the controller terminal. It may be about 10 seconds for fattree4, and a little longer for fattree8.

3) **Sanity tests** in the Mininet CLI:

```text
mininet> pingall
mininet> iperf
```

You can toggle printed metrics and adjust timers in `setting.py`:

- Discovery period (LLDP)
- Monitor period (bandwidth sampling)
- ECMP vs. Hedera scheduling thresholds
- Logging verbosity

Changes take effect on the next controller start.

---
