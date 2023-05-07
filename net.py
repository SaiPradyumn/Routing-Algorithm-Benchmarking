from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost, OVSController
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from time import time
import psutil

class RingTopo(Topo):
    def __init__(self,N,graph):
        Topo.__init__(self)
        h = []
        s = []
        delay = 5
        for i in range(N):
            a = i*2
            h.append(self.addHost('h'+str(a)))
            h.append(self.addHost('h'+str(a+1)))
            s.append( self.addSwitch('s'+str(i),stp=True,failMode='standalone'))

            self.addLink(h[a],s[i], bw=10, delay='5ms')
            self.addLink(h[a+1],s[i], bw=10, delay='5ms')

        for i in range(N-1):
            self.addLink(s[i],s[i+1], bw=10, delay='5ms')
            graph[i][i+1] = delay
            graph[i+1][i] = delay

        self.addLink(s[-1],s[0], bw=10, delay='5ms')
        graph[-1][0] = delay
        graph[0][-1] = delay

class FullyConnectedTopo(Topo):
    def __init__(self,N,graph):
        Topo.__init__(self)
        h = []
        s = []
        delay = 5
        for i in range(N):
            a = i*2
            h.append(self.addHost('h'+str(a)))
            h.append(self.addHost('h'+str(a+1)))
            s.append( self.addSwitch('s'+str(i),stp=True,failMode='standalone'))

            self.addLink(h[a],s[i], bw=10, delay='5ms')
            self.addLink(h[a+1],s[i], bw=10, delay='5ms')

        for i in range(N-1):
            for j in range(i+1,N):
                self.addLink(s[i],s[j], bw=10, delay='5ms')
                graph[i][j] = delay
                graph[j][i] = delay

class CustomFullyConnectedTopo(Topo):
    def __init__(self,N,graph):
        Topo.__init__(self)
        h = []
        s = []
        delay = 5
        for i in range(N):
            a = i*2
            h.append(self.addHost('h'+str(a)))
            h.append(self.addHost('h'+str(a+1)))
            s.append( self.addSwitch('s'+str(i),stp=True,failMode='standalone'))

            self.addLink(h[a],s[i], bw=10, delay='1ms')
            self.addLink(h[a+1],s[i], bw=10, delay='1ms')

        self.addLink(s[0],s[1], bw=10, delay='3ms')
        graph[0][1] = 3
        graph[1][0] = 3
        self.addLink(s[0],s[2], bw=10, delay='6ms')
        graph[0][2] = 6
        graph[2][0] = 6
        self.addLink(s[0],s[3], bw=10, delay='7ms')
        graph[0][3] = 7
        graph[3][0] = 7
        self.addLink(s[0],s[4], bw=10, delay='20ms')
        graph[0][4] = 20
        graph[4][0] = 20
        self.addLink(s[0],s[5], bw=10, delay='4ms')
        graph[0][5] = 4
        graph[5][0] = 4

        self.addLink(s[1],s[2], bw=10, delay='2ms')
        graph[1][2] = 2
        graph[2][1] = 2
        self.addLink(s[1],s[3], bw=10, delay='4ms')
        graph[1][3] = 4
        graph[3][1] = 4
        self.addLink(s[1],s[4], bw=10, delay='8ms')
        graph[1][4] = 8
        graph[4][1] = 8
        self.addLink(s[1],s[5], bw=10, delay='7ms')
        graph[1][5] = 7
        graph[5][1] = 7

        self.addLink(s[2],s[3], bw=10, delay='3ms')
        graph[2][3] = 3
        graph[3][2] = 3
        self.addLink(s[2],s[4], bw=10, delay='10ms')
        graph[2][4] = 10
        graph[4][2] = 10
        self.addLink(s[2],s[5], bw=10, delay='9ms')
        graph[2][5] = 9
        graph[5][2] = 9

        self.addLink(s[3],s[4], bw=10, delay='3ms')
        graph[3][4] = 3
        graph[4][3] = 3
        self.addLink(s[3],s[5], bw=10, delay='10ms')
        graph[3][5] = 10
        graph[5][3] = 10

        self.addLink(s[4],s[5], bw=10, delay='4ms')
        graph[4][5] = 4
        graph[5][4] = 4

class CustomRingTopo(Topo):
    def __init__(self,N,graph):
        Topo.__init__(self)
        N = 6
        h = []
        s = []
        for i in range(N):
            a = i*2
            h.append(self.addHost('h'+str(a)))
            h.append(self.addHost('h'+str(a+1)))
            s.append( self.addSwitch('s'+str(i),stp=True,failMode='standalone'))

            self.addLink(h[a],s[i], bw=10, delay='1ms')
            self.addLink(h[a+1],s[i], bw=10, delay='1ms')

        for i in range(4):
            self.addLink(s[i],s[i+1], bw=10, delay='1ms')
            graph[i][i+1] = 1
            graph[i+1][i] = 1

        self.addLink(s[4],s[5], bw=10, delay='5ms')
        self.addLink(s[5],s[0], bw=10, delay='5ms')
        graph[4][5] = 5
        graph[5][4] = 5
        graph[5][0] = 5
        graph[0][5] = 5

class StarTopo(Topo):
    def __init__(self,N,graph):
        Topo.__init__(self)
        h = []
        s = []
        delay = 5
        for i in range(N):
            a = i*2
            h.append(self.addHost('h'+str(a)))
            h.append(self.addHost('h'+str(a+1)))
            s.append( self.addSwitch('s'+str(i),stp=True,failMode='standalone'))

            self.addLink(h[a],s[i], bw=10, delay='5ms')
            self.addLink(h[a+1],s[i], bw=10, delay='5ms')

        switch_center = self.addSwitch('s'+str(N),stp=True,failMode='standalone')
        for i in range(N):
            self.addLink(s[i],switch_center, bw=10, delay='5ms')
            graph[i][N] = delay
            graph[N][i] = delay

def dijkstra_shortest_path(net, src, dst, graph):
    """Calculate the shortest path from src to dst using Dijkstra's algorithm"""
    shortest_path = []
    dist = {}
    prev = {}
    switches = net.switches
    unvisited = set(range(len(graph)))
    for index in unvisited:
        dist[index] = float('inf')
        prev[index] = None
    dist[src] = 0
    while unvisited:
        u = min(unvisited, key=lambda switch: dist[switch])
        unvisited.remove(u)
        if u == dst:
            while u!=src:
                shortest_path.append(switches[u])
                u = prev[u]
            shortest_path.append(switches[src])
            break

        for v in range(len(graph)):
            if(graph[u][v] == 0):
                continue
            if v in unvisited:
                alt = dist[u] + graph[u][v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    return shortest_path[::-1]

def BFS(net, src, dst, graph):
    """Calculate the shortest path from src to dst using BFS"""
    shortest_path = []
    dist = {}
    prev = {}
    switches = net.switches
    unvisited = set(range(len(graph)))
    for index in unvisited:
        dist[index] = float('inf')
        prev[index] = None
    dist[src] = 0
    while unvisited:
        u = min(unvisited, key=lambda switch: dist[switch])
        unvisited.remove(u)
        if u == dst:
            while u!=src:
                shortest_path.append(switches[u])
                u = prev[u]
            shortest_path.append(switches[src])
            break

        for v in range(len(graph)):
            if(graph[u][v] == 0):
                continue
            if v in unvisited:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    return shortest_path[::-1]

def ping(net, src, dst):
    """Ping from src to dst and return the round-trip time in ms"""
    start_time = time()
    result = net.pingFull([src, dst])
    end_time = time()
    rtt = (end_time - start_time) * 1000
    return rtt

def iperf(net, src, dst):
    """Measure the throughput from src to dst in Mbps"""
    result = net.iperf((src, dst))
    return result[0]

def packet_loss(net, src, dst):
    """Measure the packet loss rate from src to dst"""
    result = net.ping([src, dst],10)
    packet_loss_rate = result
    return packet_loss_rate

def get_cpu_memory_utilization(net):
    cpu_utilization = {}
    memory_utilization = {}
    for host in net.hosts:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        mem = psutil.virtual_memory()
        memory_percent = mem.percent
        cpu_utilization[host.name] = cpu_percent
        memory_utilization[host.name] = memory_percent
    return cpu_utilization, memory_utilization

def down_all_links(net):
    for link in net.links:
        if(link.intf1.node.name[0]!='h'):
            net.configLinkStatus(link.intf1.node.name, link.intf2.node.name, 'down')

def up_all_links(net):
    for link in net.links:
        if(link.intf1.node.name[0]!='h'):
            net.configLinkStatus(link.intf1.node.name, link.intf2.node.name, 'up')

def benchmark(net,src,dst):
    print("\n*******BENCHMARKING********")
    rtt = ping(net, src, dst)
    throughput = iperf(net, src, dst)
    packet_loss_rate = packet_loss(net, src, dst)
    cpu_utilization, memory_utilization = get_cpu_memory_utilization(net)
    print("\n*******BENCHMARK OUTPUTS*******")
    print("Ping round-trip time: "+str(rtt)+" ms")
    print("\nThroughput: "+str(throughput))
    print("\nPacket loss rate: "+str(packet_loss_rate))
    print("\nCPU Utilization:")
    for host, cpu in cpu_utilization.items():
        print(f"{host}: {cpu}")
    print("\nMemory Utilization : ",memory_utilization['h0'],"%")
    # for host, memory in memory_utilization.items():
    #     print(f"{host}: {memory}%")

def main(net,graph):

    # num_nodes = int(input("Enter N : "))

    net.start()

    # First Pingall for Network Learning I guess
    print("\nNetwork initialization ...\n")
    net.pingAll()

    src = net.get('h1')
    dst = net.get('h8')

    src_switch_index = int(src.intfList()[0].link.intf2.node.name[1:])
    dst_switch_index = int(dst.intfList()[0].link.intf2.node.name[1:])

    minimal_path = dijkstra_shortest_path(net,src_switch_index,dst_switch_index,graph)

    shortest_path = BFS(net,src_switch_index,dst_switch_index,graph)

    print("\n---------- Minimal Marginal Cost Path ----------")
    print(src.name,"-> ",end="")
    for i in minimal_path:
        print(i,"-> ",end="")
    print(dst.name)

    down_all_links(net)
    for k in range(len(minimal_path)-1):
        net.configLinkStatus(minimal_path[k].name, minimal_path[k+1].name, 'up')
        net.configLinkStatus(minimal_path[k+1].name, minimal_path[k].name, 'up')
    print("\n-------- Initial Pings  --------")
    net.ping([src]+ net.switches +[dst],timeout=10)
    print()
    benchmark(net,src,dst)

    print("\n---------------- Shortest Path -----------------")
    print(src.name,"-> ",end="")
    for i in shortest_path:
        print(i,"-> ",end="")
    print(dst.name)
    up_all_links(net)
    down_all_links(net)
    for k in range(len(shortest_path)-1):
        net.configLinkStatus(shortest_path[k].name, shortest_path[k+1].name, 'up')
        net.configLinkStatus(shortest_path[k+1].name, shortest_path[k].name, 'up')
    print("\n-------- Initial Pings  --------")
    net.ping([src]+ net.switches +[dst],timeout=10)
    print()
    benchmark(net,src,dst)

    net.stop()

# Main Body :

num_nodes = 6
graph=[[0 for i in range(num_nodes)] for j in range(num_nodes)]

# Ring Topology
# ring = RingTopo(num_nodes,graph)
# net = Mininet(topo=ring,host=CPULimitedHost, link=TCLink)
# print("Ring Topology")

# Custom Ring Topology
custom_ring = CustomRingTopo(num_nodes,graph)
net = Mininet(topo=custom_ring,host=CPULimitedHost, link=TCLink)
print("\n*-*-*-*-*-*-*-*-*-*- Custom Ring Topology -*-*-*-*-*-*-*-*-*-*")

main(net,graph)

# Fully Connected Topology
# full_connect = FullyConnectedTopo(num_nodes,graph)
# net = Mininet(topo=full_connect,host=CPULimitedHost, link=TCLink)
# print("Fully Connected Topology")

graph=[[0 for i in range(num_nodes)] for j in range(num_nodes)]
# Custom Fully Connected Topology
custom_connect = CustomFullyConnectedTopo(num_nodes,graph)
net = Mininet(topo=custom_connect,host=CPULimitedHost, link=TCLink)
print("\n\n*-*-*-*-*-*-*-*- Custom Fully Connected Topology -*-*-*-*-*-*-*-*")

main(net,graph)
