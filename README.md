TELE4642Group1

How to run mininet and setup with internet hosts

sudo python mininet_internet.py <num switches> <num_hosts>
#change line 14 of startNAT inetIntf = ' Your internet interface '
#then manually re change ip addresses of each host with ifconfig
#e.g. get connection to internet with host 11
xterm h11
ifconfig h11-eth0 0
ifconfig h11-eth0 1.0.0.1/16
route add default gw 1.0.0.254
change dns to 8.8.8.8 instead of local server
gedit /etc/resolv.conf 
# change dns google's dns 8.8.8.8 instead of 127.0.0.1
now you have connectivity on the host
