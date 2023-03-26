# Network Traffic Visualizer Using Google Maps
## Author - Matt Boraske <br> Creation Date - 3/25/23

This tool converts a network traffic packet capture into a KML file that contains global coordinate information for each IP connected to via the source machine. 
This can then be [imported into a Google Map](https://www.google.com/maps/d/) to obtain a visual overlay of the destination locations.

The example packet capture (samplePacketCapture.pcap), when converted into a KML file via the tool, produces this Google Map:
<img width="959" alt="Screenshot 2023-03-25 at 9 26 02 PM" src="https://user-images.githubusercontent.com/57207405/227750276-76050987-7f6c-4974-a223-a099a6900a1c.png">

## Instructions
1. Create a network packet traffic capture using Wireshark or a similar tool. Make sure to save the file in .pcap format
2. Run kmlGenerator.py and when it asks for a packet capture, enter the name of your .pcap file, including the file extension.
3. The output from running kmlGenerator.py is ipdata.kml. Log into [Google Maps](https://www.google.com/maps/d/) and when creating a new map, import ipdata.kml.
