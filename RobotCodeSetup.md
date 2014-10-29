RobotCodeSetup
==============

# Overview
* Image the ODROID with Linux
* Serial Login
* Networking Login
* Robot Test Setup
* Setup Robust Networking
* Bringing up `zumy_lcm_node.py`

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

7. Open http://192.168.1.122:8888/notebooks/Robot%20Test.ipynb in a browser on your laptop.
 
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
    
    exit0 
    ```
    To be clear, we're adding the `/home/bml/autostart.sh&` line.

5. Reboot, and verify that wireless is robust-ish.
    ```sh
    $ sudo shutdown -r 0
    ```

## Bringing up `zumy_lcm_node.py`
1. Install LCM:

    see https://code.google.com/p/lcm/wiki/BuildInstructions and https://github.com/lcm-proj/lcm/blob/master/INSTALL
    ```sh
    $ sudo apt-get install build-essential libglib2.0-dev openjdk-6-jdk python-dev checkinstall autoconf autopoint libtool python-psutil
    $ sudo pip install psutil --upgrade
    $ wget https://github.com/lcm-proj/lcm/archive/v1.1.2.tar.gz
    $ tar xzvf v1.1.2.tar.gz
    $ cd lcm-1.1.2
    $ ./bootstrap.sh
    $ ./configure
    $ make -j4
    $ sudo checkinstall (install package as lcm)
    $ sudo ldconfig
    ```
2. Configure Your Networking for LCM:

    When using more than one network interface, (ie. eth0 and wlan0), be sure to manually specify the route for the udp multicast address.
    For example:
    ```sh
    ajc@rektjc:~$ route
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    default         10.10.64.1      0.0.0.0         UG    0      0        0 wlan0
    10.10.64.0      *               255.255.252.0   U     2      0        0 wlan0
    10.42.0.0       *               255.255.255.0   U     1      0        0 eth0
    link-local      *               255.255.0.0     U     1000   0        0 eth0
    192.168.1.0     *               255.255.255.0   U     2      0        0 wlan2
    192.168.56.0    *               255.255.255.0   U     0      0        0 vboxnet0
    239.255.76.67   *               255.255.255.255 UH    0      0        0 wlan2
    ```
    Setup in Network Manager:
    Right click Network Manager Applet > Edit Connections > Wireless > fearing-robonet > IPv4 Settings > Routes... > Add "Address"=239.255.76.67, "Netmask"=255.255.255.255, leave "Gateway" and "Metric" blank.
"Use this connection only for resources on its network" works if you want to connect to the internet with another interface.

3. Name the robot's id:
    ```sh
    $ echo '/040' > ~/zc_id
    ```

4. generate lcm types:
    ```sh
    $ cd ~/zumy
    $ ./gen_types.sh
    ```

5. run `zumy_lcm_node.py`
    ```sh
    $ python ~/zumy/python/zumy_lcm_node.py
    ```

6. In a separate terminal on the robot, run:
    ```sh
    $ cd ~/zumy/notebook/
    $ ipython notebook --ip=* --no-browser
    ```

7. Open http://192.168.1.122:8888/notebooks/Zumy%20LCM%20Node%20Test.ipynb in a browser window.

8. Edit `start_scripts/odroid_init.sh`, see this:
    ```
    #!/bin/bash
    #
    # This script needs to be run by /etc/rc.local on the ODROID.
    #
    
    su -l bml -c 'screen -S linux_state -d -m python /home/bml/zumy/python/linux_state_pub.py'
    
    su -l bml -c 'screen -S zumy_lcm_node -d -m python /home/bml/zumy/python/zumy_lcm_node.py'
    
    screen -S netstarter -d -m python /home/bml/zumy/python/netstarter.py
    ```
    The line with `zumy_lcm_node` should autostart `zumy_lcm_node.py` on boot.
    
9. Reboot the robot, and run `lcm_spy.sh` to see some diagnostic messages from the robot.
