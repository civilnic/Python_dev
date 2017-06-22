import sys
from scapy.all import *
import pcapy
import impacket.ImpactDecoder as Decoders
import impacket.ImpactPacket as Packets


def main():

    reader = pcapy.open_offline("mydata.pcap")
    eth_decoder = Decoders.EthDecoder()
    ip_decoder = Decoders.IPDecoder()
    udp_decoder = Decoders.UDPDecoder()
    while True:
        try:
            (header, payload) = reader.next()
            ethernet = eth_decoder.decode(payload)
        if ethernet.get_ether_type() == Packets.IP.ethertype:
            ip = ip_decoder.decode(payload[ethernet.get_header_size():])
        if ip.get_ip_p() == Packets.UDP.protocol:
            udp = udp_decoder.decode(
        payload[ethernet.get_header_size()+ip.get_header_size():])
                        print("IPv4 UDP packet %s:%d->%s:%d" % (ip.get_ip_src()),
                        udp.get_uh_sport(),
                        ip.get_ip_dst(),
                        udp.get_uh_dport())
        except pcapy.PcapError:
            break

main()