import sys
from scapy.all import *

def main():

    # do something with the packet
    #filtered = (pkt for pkt in packets if "UDP" in pkt)

    packets = rdpcap('20170622_TCAS_03_ALLSAMPLE_10ms.pcap')
  #  print(packets)
#    for packet in packets:
 #       packet.show()
    print(packets.filter(lambda p: p[UDP].dport==8913))
    packets=packets.filter(lambda p: p[UDP].dport==8913)
    #packets[0].show()





    # Rewrite the packets with the new addresses
    for p in packets:
        if p.haslayer(IP):
            del p[IP].chksum
            p[Ether].dst = "44:39:C4:37:F6:FC"
            #[Ether].src = "44:39:C4:37:F6:FC"
            #p[Ether].dst = "00:00:00:00:00:00"
            #p[Ether].src = "00:00:00:00:00:00"
            #p[IP].src = "127.0.0.1"
            p[IP].dst = "10.25.92.125"
            #p[UDP].dport = 4999

            sendp(p)

    #packets[0].show()
#    for packet in packets:
#        packet.show()
    #packets.summary()
    wrpcap("20170622_TCAS_03_ALLSAMPLE_10ms_modifie.pcap", packets)
main()