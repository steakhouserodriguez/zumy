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

Downloaded images from: http://odroid.in/ubuntu_14.04lts/

```bash
user@dev-machine:~$ wget http://odroid.in/ubuntu_14.04lts/ubuntu-14.04lts-server-odroid-u-20140604.img.xz
user@dev-machine:~$ wget http://odroid.in/ubuntu_14.04lts/ubuntu-14.04lts-server-odroid-u-20140604.img.xz.md5sum
user@dev-machine:~$ md5sum ubuntu-14.04lts-server-odroid-u-20140604.img.xz
user@dev-machine:~$ cat disk_images/ubuntu-14.04lts-server-odroid-u-20140604.img.xz.md5sum
user@dev-machine:~$ xzcat ubuntu-14.04lts-server-odroid-u-20140604.img.xz | sudo dd of=/dev/mmcblk0 bs=4M
user@dev-machine:~$ sync
```


## Serial Login
```sh
user@dev-machine:~$ sudo apt-get install screen
user@dev-machine:~$ sudo screen /dev/ttyUSB0 115200
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

auto wlan0
iface wlan0 inet static
address 192.168.1.66
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 192.168.1.1 8.8.8.8
wpa-ssid fearing-robonet
wpa-psk fearingrobonet
```

You may need to comment out the contents of /etc/network/interfaces.d/eth0:

```sh
## /etc/network/interfaces.d/eth0
# auto eth0
# iface eth0 inet dhcp
```
1. Check the network device names:
    ```sh
    root@odroid-server:~$ ifconfig -a
    ```

2. Edit these files with nano:
    ```sh
    root@odroid-server:~$ nano /etc/network/interfaces
    root@odroid-server:~$ nano /etc/network/interfaces.d/eth0
    ```

3. Manually bring up the network and test:
    ```sh
    root@odroid-server:~$ ifup wlan0
    root@odroid-server:~$ ping 192.168.1.1
    ```
    You should be able to ping the robot from your development machine:
    ```sh
    user@dev-machine:~$ ping 192.168.1.66
    ```

3. Do a reboot test:
    ```sh
    root@odroid-server:~$ shutdown -h 0
    ```
    Check that the robot is reachable from your development machine:
    ```sh
    user@dev-machine:~$ ping 192.168.1.66
    ```

N.B: wireless adapters are given unique interface names (ie. wlan0, wlan1) based on their MAC addresses, so once the boards are configured, the wireless adapters cannot be arbitrarily swapped.

### Add a user
As root in the serial terminal:
```sh
root@odroid-server:~$ adduser bml           # adds the user
root@odroid-server:~$ gpasswd -a bml sudo   # adds bml to group sudo, granting administrator privledges
```

### Install openssh server for network login

```sh
root@odroid-server:~$ sudo apt-get install openssh-server
```
After this, you should be able to login to the board over the network using

```sh 
user@dev-machine:~ $ sudo apt-get install openssh-client   # run this on the ground station
user@dev-machine:~ $ ssh bml@192.168.1.66                 # run this on the ground station
```

## Robot Test Setup
1. Add permissions to use serial devices
  ```ssh
  bml@odroid-server:~$ sudo gpasswd -a bml dialout
  ```

2. Reboot for permissions to reset
  ```sh
  bml@odroid-server:~$ sudo shutdown -h 0
  ```

3. Install package requirements for zumy ipython node
  ```sh
  bml@odroid-server:~$ sudo ntpdate ntp.ubuntu.com                         # https doesn't work if the time isn't synced.
  bml@odroid-server:~$ sudo apt-get install python-dev python-pip ipython-notebook python-serial python-numpy python-scipy byobu git
  bml@odroid-server:~$ sudo pip install ipython[notebook] --upgrade
  ```

4. Launch byobu (allows you to run a persistent, multiplexed terminal session)
  ```sh
  bml@odroid-server:~$ byobu
  ```

5. Clone the 'zumy' repo:
  ```sh
  bml@odroid-server:~$ sudo ntpdate ntp.ubuntu.com      # https doesn't work if the time isn't synced.
  bml@odroid-server:~$ git clone https://github.com/andrewjchen/zumy.git
  bml@odroid-server:~$ cd zumy
  ```

6. In byobu, launch ipython notebook:
  ```sh
  bml@odroid-server:~/zumy$ ipython notebook --ip=* --no-browser
  ```

7. Open http://192.168.1.66:8888 in a browser on your laptop, navigate to zumy > notebooks > Robot Test
 
## Setup Robust Networking
1. Install `netstarter.py` dependencies:
    ```sh
    bml@odroid-server:~$ sudo ntpdate ntp.ubuntu.com          # https doesn't work if the time isn't synced.
    bml@odroid-server:~$ sudo pip install netifaces
    ```

2. Test the restarting script:
    ```sh
    bml@odroid-server:~$ sudo python ~/zumy/python/netstarter.py
    ```

3. Make a symblink:
    ```sh
    bml@odroid-server:~$ ln -s ~/zumy/start_scripts/odroid_init.sh ~/autostart.sh
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
    bml@odroid-server:~$ sudo shutdown -h 0
    ```

## Bringing up `zumy_lcm_node.py`
1. Install LCM:

    see https://code.google.com/p/lcm/wiki/BuildInstructions and https://github.com/lcm-proj/lcm/blob/master/INSTALL
    ```sh
    bml@odroid-server:~$ sudo apt-get install build-essential libglib2.0-dev openjdk-6-jdk python-dev checkinstall autoconf autopoint libtool python-psutil
    bml@odroid-server:~$ sudo ntpdate ntp.ubuntu.com          # https doesn't work if the time isn't synced.
    bml@odroid-server:~$ sudo pip install psutil --upgrade
    bml@odroid-server:~$ wget https://github.com/lcm-proj/lcm/archive/v1.1.2.tar.gz
    bml@odroid-server:~$ tar xzvf v1.1.2.tar.gz
    bml@odroid-server:~$ cd lcm-1.1.2
    bml@odroid-server:~/lcm-1.1.2$ ./bootstrap.sh
    bml@odroid-server:~/lcm-1.1.2$ ./configure
    bml@odroid-server:~/lcm-1.1.2$ make -j4
    bml@odroid-server:~/lcm-1.1.2$ sudo checkinstall #(install package as lcm)
    bml@odroid-server:~/lcm-1.1.2$ sudo ldconfig
    ```

2. Name the robot's id:
    ```sh
    bml@odroid-server:~$ echo '/040' > ~/zc_id
    bml@odroid-server:~$ sudo nano /etc/hostname # rename odroid-server to zumy044
    bml@odroid-server:~$ sudo nano /etc/hosts # rename odroid-server to zumy044
    ```

3. copy lcm.jar to zumy:
    ```sh
    bml@odroid-server:~$ cp lcm-1.1.2/lcm-java/lcm.jar ~/zumy/
    ```

4. generate lcm types:
    ```sh
    bml@odroid-server:~$ cd ~/zumy
    bml@odroid-server:~/zumy$ ./gen_types.sh
    ```

5. run `zumy_lcm_node.py`
    ```sh
    bml@odroid-server:~$ python ~/zumy/python/zumy_lcm_node.py
    ```

6. In a separate terminal on the robot, run:
    ```sh
    bml@odroid-server:~$ ipython notebook --ip=* --no-browser
    ```

7. Open http://192.168.1.66:8888/ in a browser window, navigate through zumy > notebooks > Zumy LCM Node Test

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
    
9. Reboot the robot, See [Ground Station Setup](GroundStationSetup.md) and setup LCM, and try running `lcm-spy.sh` to see the messages the robot broadcasts.
