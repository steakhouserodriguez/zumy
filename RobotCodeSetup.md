RobotCodeSetup
==============

# Overview
* Image the ODROID with Linux
* Serial Login
* Networking Login
* Robot Test Setup
* Setup Robust Networking

## ODROID imaging
http://nbviewer.ipython.org/github/biomimetics/bml_tools/blob/master/arm_linux/odroid_imaging.ipynb

## Serial Login
```sh
$ screen /dev/ttyUSB0 115200
```

## Network Login
Networking login requires network configuration and installing ssh.

### Networking

Configure the networking settings using the serial terminal.
The robot linux boards are configured using manual networking, defined under `/etc/network/interfaces`.

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

1. Edit these files with nano:
    ```sh
    $ nano /etc/network/interfaces
    $ nano /etc/networking/interfaces.d/eth0
    ```

2. Reboot the board:
    ```sh
    $ shutdown -r 0
    ```

3. On your development machine, you should be able to ping the machine:
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
  $ sudo apt-get install python-dev python-pip ipython-notebook python-serial python-numpy python-scipy byobu git
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
  $ ipython notebook --ip=* --no-browser
  ```

7. Open http://192.168.1.122:8888 in a browser on your laptop
8. Follow the instructions in the Robot Test.ipynb notebook.
 
## Setup Robust Networking
1. Install `netstarter.py` dependencies:
    ```sh
    $ sudo pip install netifaces
    ```

2. Test the restarting script:
    ```sh
    $ sudo python ~/zumy/python/netstarter.py
    ```

3. Make a symblink:
    ```sh
    $ ln -s ~/zumy/start_scripts/odroid_init.sh ~/autostart.sh
    ```
    This will make it easy to change the code that runs on boot.

4. Setup the script to run automatically at boot:
    Edit `/etc/rc.local`:
    ```
    #!/bin/sh -e
    #
    # rc.local
    #
    # This script is executed at the end of each multiuser runlevel.
    # Make sure that the script will "exit 0" on success or any other
    # value on error.
    #
    # In order to enable or disable this script just change the execution
    # bits.
    #
    # By default this script does nothing.
    
    /home/bml/autostart.sh&
    
    exit 0
    ```
    To be clear, we're adding the `/home/bml/autostart.sh&` line.

5. Reboot, and verify that wireless is robust-ish.
    ```sh
    $ sudo shutdown -r 0
    ```
