RobotCodeSetup
==============

# Overview
* Image the ODROID with Linux
* Serial Login
* Setup Networking
* Add a user
* Install useful software
* Install LCM


## ODROID imaging
http://nbviewer.ipython.org/github/biomimetics/bml_tools/blob/master/arm_linux/odroid_imaging.ipynb

## Serial Login
1. Plug in the USB-UART cable; UART into the ODROID, USB into your laptop.
 <img src="http://dn.odroid.com/homebackup/201206301837550501.jpg" height="100" width="100">

2. Log in using screen  
  ```sh
  $ screen /dev/ttyUSB0 115200
  ```
3. Press Enter, you should see a root terminal.


## Setup Networking
Configure the networking settings using the serial terminal.
The robot linux boards are configured using manual networking, defined under /etc/network/interfaces.

Example settings:

```sh
# /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback
#auto eth0
# iface eth0 inet dhcp

auto wlan1
iface wlan1 inet static
address 192.168.1.122
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 192.168.1.1 8.8.8.8
wpa-ssid fearing-robonet
wpa-psk fearingrobonet
```

You may need to comment out the contents of /etc/network/interfaces.d/eth0:

```sh
## /etc/networking/interfaces.d/eth0
# auto eth0
# iface eth0 inet dhcp
```

N.B: wireless adapters are given unique interface names (ie. wlan0, wlan1) based on their MAC addresses, so once the boards are configured, the wireless adapters cannot be arbitrarily swapped.

Now, reboot the board:
```sh
$ shutdown -r 0
```

On your development machine, you should be able to ping the machine:
```sh
$ ping 192.168.1.122
```

## Add a user
As root in the serial terminal:
```sh
$ adduser bml           # adds the user
$ gpasswd -a bml sudo   # adds bml to group sudo, granting administrator privledges
```

## Install useful software

```sh
$ sudo apt-get install openssh-server
```
After this, you should be able to login to the board using

```sh
$ ssh bml@192.168.1.122
```

## Install LCM
LCM build instructions found here:
https://code.google.com/p/lcm/wiki/BuildInstructions


