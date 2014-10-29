RobotCodeSetup
==============

# Overview
* Image the ODROID with Linux
* Serial Login
* Networking Login
* Robot Test Setup


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


## Network Login
Networking login requires network configuration and installing ssh.

### Networking

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

Now, reboot the board:
```sh
$ shutdown -r 0
```

On your development machine, you should be able to ping the machine:
```sh
$ ping 192.168.1.122
```

N.B: wireless adapters are given unique interface names (ie. wlan0, wlan1) based on their MAC addresses, so once the boards are configured, the wireless adapters cannot be arbitrarily swapped.

### Add a user
As root in the serial terminal:
```sh
$ adduser bml           # adds the user
$ gpasswd -a bml sudo   # adds bml to group sudo, granting administrator privledges
```

### Install openssh server for network login

```sh
$ sudo apt-get install openssh-server
```
After this, you should be able to login to the board over the network using

```sh
$ ssh bml@192.168.1.122
```

## Robot Test Setup
1. Add permissions to use serial devices
  ```ssh
  $ sudo gpasswd -a bml dialout
  ```

2. Reboot for permissions to reset
  ```sh
  $ sudo shutdown -h 0
  ```

3. Install package requirements for zumy ipython node
  ```sh
  $ sudo apt-get install python-pip ipython-notebook python-serial python-numpy python-scipy byobu git
  ```

4. Launch byobu (allows you to run a persistent, multiplexed terminal session)
  ```sh
  $ byobu
  ```

5. Clone the 'zumy' repo:
  ```sh
  $ sudo ntpdate ntp.ubuntu.com                         # https doesn't work if the time isn't synced.
  $ git clone https://github.com/andrewjchen/zumy.git
  $ cd zumy
  $ git checkout redoc
  ```

6. In byobu, launch ipython notebook:
  ```sh
  $ cd ~/zumy/notebook
  $ ipython notebook ip=*
  ```

7. Open http://192.168.1.122:8888 in a browser on your laptop
8. Follow the instructions in the RobotCodeSetup.ipynb notebook.
 

