  GNU nano 7.2                                         bash_script1.sh                                                  #!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <MAC_ADDRESS> [POINT]"
  exit 1
fi

DEFAULT_POINT="(0,0)"
mac="$1"
point=${2:-$DEFAULT_POINT}

# Run tcpdump and process with tshark
sudo tcpdump -l -i wlan0 ether host "$mac" -w - | \
tshark -r - -Y "(wlan.sa == $mac)" -T fields \
    -E separator=';' -E quote=d \
    -e frame.time -e wlan.sa -e wlan.da -e radiotap.dbm_antsignal | \
awk -v point="$point" -F';' '{
    gsub(/\"/, "", $1);  
    print $1, $2, $3, $4, point;
}' | python endpoint_script.py
