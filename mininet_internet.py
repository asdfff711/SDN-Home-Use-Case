#!/usr/bin/python

import sys
import re
from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeTopo
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.util import irange,dumpNodeConnections
#################################
def startNAT( root, subnet, sw, inetIntf='wlp1s0' ):
    """Start NAT/forwarding between Mininet and external network
    root: node to access iptables from
    inetIntf: interface for internet access
    subnet: Mininet subnet (default 11.0/8)="""

    # Identify the interface connecting to the mininet network
    #localIntf =  root.defaultIntf()
    localIntf = root.intf('root-eth'+str(sw-1))
    # print "localIntf::: %s  for subnet:: %s in switch:: %s" % (localIntf,subnet,sw)

    # Configure NAT
    root.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet, '-j DROP' )
    root.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )


    # Instruct the kernel to perform forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=1' )

def stopNAT( root ):
    """Stop NAT/forwarding between Mininet and external network"""
    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Instruct the kernel to stop forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=0' )


def fixNetworkManager( root, intf ):
    """Prevent network-manager from messing with our interface,
       by specifying manual configuration in /etc/network/interfaces
       root: a node in the root namespace (for running commands)
       intf: interface name"""
    cfile = '/etc/network/interfaces'
    line = '\niface %s inet manual\n' % intf
    config = open( cfile ).read()
    if ( line ) not in config:
        print '*** Adding', line.strip(), 'to', cfile
        with open( cfile, 'a' ) as f:
            f.write( line )
        # Probably need to restart network-manager to be safe -
        # hopefully this won't disconnect you
        root.cmd( 'service network-manager restart' )

def connectToInternet( network, nswitches, nhosts, dpid_list ):
    """Connect the network to the internet
       switch: switch to connect to root namespace
       rootip: address for interface in root namespace
       subnet: Mininet subnet"""


    # Create a node in root namespace
    root = Node( 'root', inNamespace=False )
    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Create default entries for unmatched traffic
    root.cmd( 'iptables -P INPUT ACCEPT' )
    root.cmd( 'iptables -P OUTPUT ACCEPT' )
    root.cmd( 'iptables -P FORWARD DROP' )
    # print " Before Restart"
    # root.cmd( 'service isc-dhcp-server restart' )


    for sw in irange(1,nswitches):
        switch = network.get('s%s' % sw)
        subnet = str(sw)+'.0/8'
        prefixLen = subnet.split('/')[1]



        # Prevent network-manager from interfering with our interface
        # fixNetworkManager( root, 'root-ens33' )

        # Create link between root NS and switch
        link = network.addLink( root, switch)
        # print "link::::", link
        link.intf1.setIP( str(sw)+'.254', prefixLen )
        link.intf1.setMAC('a4:a5:2f:02:01:'+str('{:02X}'.format(sw)))

        # Start network that now includes link to root namespace
        network.start()

        # Start NAT and establish forwarding
        startNAT( root, subnet, sw)

        # Establish routes from end hosts
        nw_hosts = network.hosts
        # print "nw_hosts:::::", nw_hosts
        for host in network.hosts:
            if re.search('h%s' %sw ,str(host)):
                # print "For host::%s in Switch: %s"%(str(host),str(sw))
                host.cmd( 'ip route flush root 0/0' )
                host.cmd( 'route add -net', subnet, 'dev', host.defaultIntf() )
                host.cmd( 'route add default gw', str(sw)+'.254' )




    # for host in network.hosts:
    #     h_id = str(host)
    #     # printclear
    #     host.cmd('hostnamectl --static   set-hostname switch'+h_id[1:2]+'-host'+h_id[2:])



    for switch in network.switches:
        sw = str(switch)
        vx_name = sw[1:]
        # print vx_name
        switch.cmd('ovs-vsctl add-port '+ sw + ' tun-vxlan'+vx_name + ' -- set interface tun-vxlan'+vx_name+' type=vxlan options:remote_ip=129.94.5.125 options:key=0x0201'+str('{:02X}'.format(int(vx_name))))
        # switch.cmd('ovs-vsctl add-port '+ sw + ' tun-vxlan -- set interface tun-vxlan type=vxlan options:remote_ip=129.94.5.125 options:key=0xe00c'+str('{:02X}'.format(int(vx_name))))
    #     print('ovs-ofctl add-flow '+sw+' priority=5,actions=output:'+str(nhosts+2)+',normal -O OpenFlow13')
        # switch.cmd('ovs-ofctl add-flow '+sw+' priority=5,udp,tp_dst=53,actions=output:'+str(nhosts+2)+',normal -O OpenFlow13')
        switch.cmd('ovs-ofctl add-flow '+sw+' priority=5,actions=output:'+str(nhosts+2)+',normal -O OpenFlow13')
    #     # switch.cmd('ovs-ofctl add-flow s2 priority=5,actions=output:'+str(nhosts+2)+',normal -O OpenFlow13')



    return root


if __name__ == '__main__':
    lg.setLogLevel( 'info')

    nswitches = int(sys.argv[1])
    nhosts = int(sys.argv[2])

    net = Mininet( topo=None, build=False)
    net.addController('c1',controller=RemoteController,ip='127.0.0.1',port=55555)
    # net.addController('c1',controller=RemoteController,ip='127.0.0.1',port=6653)
    dpid_list = []
    for sw in irange(1,nswitches):
        vx_dpid = str('{:06X}'.format(sw))
        dpid_list.append(vx_dpid)
        # switch = net.addSwitch('s%s' % sw, dpid = dpid)
        # switch = net.addSwitch('s%s' % sw, dpid = str('{:016X}'.format(sw)), mac = '00:'+str('{:02X}'.format(sw))+':00:00:00:00:00:'+str('{:02X}'.format(sw)))
        switch = net.addSwitch('s%s' % sw, dpid = '0101a4a52f0201'+ str('{:02X}'.format(sw)))
        print "Adding Switch with dpid = " +'0101a4a52f0201' +str('{:02X}'.format(sw))
        for h in irange(1,nhosts):
            host = net.addHost('h'+str(sw)+str(h), mac = '00:'+str('{:02X}'.format(sw))+':00:00:00:' + str('{:02X}'.format(h)))
            # host = net.addHost('h'+str(sw)+str(h),ip = str(sw)+'.0.0.'+str(h), mac = '00:'+str('{:02X}'.format(sw))+':00:00:00:' + str('{:02X}'.format(h)))
            net.addLink(switch, host)
            print "Adding Host with mac = " + '00:'+ str('{:02X}'.format(sw))+':00:00:00:'+ str('{:02X}'.format(h))

    # print dpid_list

    # Configure and start NATted connectivity
    rootnode = connectToInternet(net, nswitches, nhosts, dpid_list)
    print "*** Hosts are running and should have internet connectivity"
    print "*** Type 'exit' or control-D to shut down network"

    host11 = net.hosts[0]
    host11.cmd('ifconfig h11-eth0 1.0.0.1/16')
    host11.cmd('route add default gw 1.0.0.254')
     
    CLI( net )

    # Shut down NAT
    stopNAT( rootnode )
    net.stop()
