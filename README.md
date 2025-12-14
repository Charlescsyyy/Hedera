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

## For MAC
If you want to run the code with Mac, we suppose you to use introductions below:

```markdown
# Hedera Demo — Run Guide (Mininet + Ryu)

This README explains how to run the Hedera demo using a Docker-based Mininet + Ryu environment.

## Prerequisites
- Docker installed on your host machine.
- A container named `mininet-dev` that includes Mininet and Ryu, with this codebase available inside (e.g., at `ryu/ryu/app/Hedera/`).

## Quick Start

### 1) Start the Docker container
```bash
docker start mininet-dev
```

### 2) Attach to the container shell
```bash
docker exec -it mininet-dev /bin/bash
```

It’s recommended to use two terminal sessions:
- Terminal A: run the Ryu controller.
- Terminal B: run the Mininet topology and tests.

### 3) Launch the Fat-Tree topology (Terminal B)
From inside the container:
```bash
sudo python ryu/ryu/app/Hedera/fattree4.py
```
This starts a Fat-Tree (fanout=4) topology and drops you into the Mininet CLI.

### 4) Start the Ryu controller (Terminal A)
Navigate to the Hedera app directory (adjust path as needed):
```bash
cd ryu/ryu/app/Hedera
```

Run with default settings:
```bash
ryu-manager --observe-links ./Hedera.py
```

Or run with explicit parameters:
```bash
ryu-manager --observe-links ./Hedera.py --k_paths=4 --weight=hop --fanout=4
```

### 5) Verify connectivity (Terminal B — Mininet CLI)
```bash
mininet> pingall
```
Optionally generate traffic (e.g., iperf) to observe path selection and monitoring behavior.

### 6) Cleanup
From inside the container:
```bash
sudo mn -c
```
Optionally stop the container:
```bash
docker stop mininet-dev
```

## Command Reference

- Start container:
  ```bash
  docker start mininet-dev
  ```
- Attach shell:
  ```bash
  docker exec -it mininet-dev /bin/bash
  ```
- Launch Fat-Tree (fanout=4):
  ```bash
  sudo python ryu/ryu/app/Hedera/fattree4.py
  ```
- Clear Mininet state:
  ```bash
  sudo mn -c
  ```
- Run Ryu (default):
  ```bash
  ryu-manager --observe-links ./Hedera.py
  ```
- Run Ryu (custom):
  ```bash
  ryu-manager --observe-links ./Hedera.py --k_paths=4 --weight=hop --fanout=4
  ```

## Parameters

- `--observe-links`: enables Ryu’s topology discovery (switches, links, hosts).
- `--k_paths=4`: number of precomputed equal-cost shortest paths to consider.
- `--weight=hop`: path cost metric (hop-based).
- `--fanout=4`: fanout used for the Fat-Tree topology.

## Tips & Troubleshooting

- Use two terminals: one for Ryu, one for Mininet CLI.
- If `Hedera.py` or `fattree4.py` isn’t found, ensure you are in `ryu/ryu/app/Hedera` and paths match your repo layout.
- If Mininet reports stale state or fails to start, run `sudo mn -c` and retry.
- Some operations require root in the container; prepend `sudo` where necessary.
- Ensure `ryu-manager` is in PATH; if not, confirm Ryu is installed inside the container.

```

Changes take effect on the next controller start.

---
