
Network drive: pi 
password: raspberry

WIFI NETWORK:
Network name: MdpGrp10 
password:     2013Grp0


SET A						    SET B							
------                          -------
rpi address: 192.168.10.10		rpi address: 192.168.10.10
range start: 192.168.10.1		range start: 192.168.10.11
range end  : 192.168.10.9		range end  : 192.168.10.255


PC
--------
tcpkill -i wlan0 port 5182


Bluetooth
--------
**Inside python script**
subprocess.Popen(['sh','./blueReset.sh'])    

**Inside RPI**
sudo chmod +x  blueReset.sh 
------------------------------
pkill blueman-applet
sudo hciconfig hci0 piscan
------------------------------

--Change Rpi bluetooth name--
sudo hciconfig hci0 name 'Device Name'

--Bluetooth status--
/etc/init.d/bluetooth status

--Enable Rpi bluetooth discovery--
sudo bluez-test-adapter discoverable on

--Scan for available bluetooth devices--
hcitool scan
bluez-test-device list


--Connecting to device--
sudo bluez-simple-agent hci0
sudo bluez-test-device trusted       yes
sudo bluez-test-input connect



Arduino
=========
sudo apt-get install python-serial




