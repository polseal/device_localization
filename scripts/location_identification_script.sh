  GNU nano 7.2                                         bash_script1.sh                                                  #!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <MAC_ADDRESS> <POINT>"
  exit 1
fi

mac="$1"
point="$2"

timeout 60 sudo tcpdump -i wlan0 ether host "$mac" -w ~/Desktop/device_traffic.pcap

tshark -r ~/Desktop/device_traffic.pcap -Y "wlan.sa == $mac || wlan.da == $mac" -T fields \
    -e frame.time -e wlan.sa -e wlan.da -e radiotap.dbm_antsignal | \
awk -v point="$point" '{print $0 "," point}' | \
python script_python.py rssi_values.csv
