  GNU nano 7.2                                         monitor_mode.sh                                                  #!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <interface>"
  exit 1
fi

interface=$1

echo "Bringing $interface down..."
sudo ifconfig $interface down

echo "Setting $interface to monitor mode..."
sudo iwconfig $interface mode monitor

echo "Bringing $interface up..."
sudo ifconfig $interface up

echo "$interface is now in monitor mode."