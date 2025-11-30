from time import sleep
from mininet.node import RemoteController
from mininet.cli import CLI

def simulate_traffic_fattree(net):
    print("FatTree4 network instance connected, starting traffic simulation...")

    try:
        h001 = net.get('h001')
        h005 = net.get('h005')
        h006 = net.get('h006')
        h003 = net.get('h003')
        h002 = net.get('h002')
    except KeyError as e:
        print(f" ERROR: Unable to retrieve host: {e}")
        return

    print("\nSimulating elephant flow (2 Mbps): h001 -> h005 [UDP]")
    h005.cmd('iperf -s -u > h005_server.log &')
    h001.cmd('iperf -c {} -u -b 2M -t 30 > h001_to_h005.log &'.format(h005.IP()))

    print("\nSimulating elephant flow (3 Mbps): h002 -> h006 [UDP]")
    h006.cmd('iperf -s -u > h006_server.log &') 
    h002.cmd('iperf -c {} -u -b 3M -t 30 > h002_to_h006.log &'.format(h006.IP()))

    print("\nSimulating mice flow (0.5 Mbps): h003 -> h005")
    h003.cmd('iperf -c {} -u -b 0.5M -t 10 > h003_to_h005.log &'.format(h005.IP()))

    print("\nTraffic simulation is in progress. Please wait 30 seconds to view the results...")
    sleep(35)

    print("\nTraffic simulation completed. Check log files for analysis:")
    print("- h001_to_h005.log, h002_to_h006.log, h003_to_h005.log, h005_server.log")

    CLI(net)

if __name__ == "__main__":
    from mininet.net import Mininet

    print("Attempting to retrieve the running Mininet network instance...")
    try:
        net = Mininet.init()
        simulate_traffic_fattree(net)
    except Exception as e:
        print(f"Error: Unable to retrieve the Mininet network instance. Make sure Mininet is running and the FatTree4 network is initialized. Error details: {e}")