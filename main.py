# Network Traffic Packet Visualizer
# Author: @MattBoraske
#
# Dependencies: dpkt, pygeoip, requests
#
# Description: This script will take a packet capture file and 
#              create a KML file that can be used to plot the 
#              source and destination IP addresses on a Google Earth map.
#
# Note: A packet capture file (.pcap) is needed as input for this script. 
#       One tool that you can use to create a packet capture file is Wireshark.

import socket #https://docs.python.org/3/library/socket.html
import dpkt #https://dpkt.readthedocs.io/en/latest/
from pygeoip import GeoIP #https://pypi.org/project/pygeoip/
import requests #https://www.w3schools.com/python/module_requests.asp

# GeoIP database
gi = GeoIP('maxmind.dat') #https://www.miyuru.lk/geoiplegacy - download the MaxMind - City IPv6/IPv4 .dat file

# Get the source IP address
SOURCE_IP = requests.get('https://api.ipify.org').content.decode('utf8')

def main():
    packetCapture = input("Enter the name of the packet capture file: ")
    f = open(packetCapture, 'rb')
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter

    with open("ipdata.kml", "w") as file:
        file.write(kmldoc)
    print(kmldoc)
    print(f"source ip: {SOURCE_IP}")

if __name__ == '__main__':
    main()

def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts

def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name(SOURCE_IP)
    #src = gi.record_by_name('174.198.18.60')
    #print("\t\tgi src: ", src)
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''


