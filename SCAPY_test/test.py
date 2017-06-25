import sys
from scapy.all import *

def main():

    # do something with the packet
    #filtered = (pkt for pkt in packets if "UDP" in pkt)

    packets = rdpcap('20170622_TCAS_03_ALLSAMPLE_10ms.pcap')
    print(packets)
#    for packet in packets:
 #       packet.show()
    packets
    print(packets.filter(lambda p: p[UDP].dport==8913))
    packets=packets.filter(lambda p: p[UDP].dport==8913)
    packets[0].show()

    packets[0][UDP].dport = 4999

    for p in packets:
        del p[IP].chksum

    # Rewrite the packets with the new addresses
    for p in packets:
        if p.haslayer(IP):
            p[IP].src = '10.25.93.125'
            p[IP].dst = '10.25.93.125'

    packets[0].show()
#    for packet in packets:
#        packet.show()
    #packets.summary()
    wrpcap("20170622_TCAS_03_ALLSAMPLE_10ms_modifie.pcap", packets)
main()