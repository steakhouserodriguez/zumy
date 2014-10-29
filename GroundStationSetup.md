Ground Station Setup
====================
Ground station = development machine.

# Overview
* Useful Software
* LCM
* IPython
* ROS

## Useful Software

#### byobu
byobu is a terminal multiplexer.
```sh
$ byobu
```
* F2: New tab
* F3: Previous Tab
* F4: Next Tab
* F6: Detach

#### ssh
ssh lets you log into a robot over the network
```sh
$ ssh bml@192.168.1.122
```

For keyed login:
```sh
$ ssh-keygen #if you do not have an existing key
$ ssh-copy-id bml@192.168.1.122
```
this will allow you to use any ssh service without a password. 

#### ping
ping lets you check network connectivity
```sh
$ ping 192.168.1.122
```

#### rsync
rsync can be used to send your code to the robot.
```sh
$ rsync -avi . bml@192.168.1.122:/home/bml/zumy
```

#### sshfs
sshfs lets you mount the robot's filesystem locally.
```sh
$ mkdir 122
$ sshfs bml@192.168.1.122:/home/bml 122
$ ls 122
```

## LCM

### Build & Setup Instructions
(copied from [Robot Code Setup](RobotCodeSetup.md))

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

3. Copy `lcm.jar` to `zumy`:
    ```sh
    cp lcm-1.1.2/lcm.jar zumy/
    ```
  This will enable packet inspection.

### Useful Scripts

#### `lcm_spy.sh`: lcm packet introspection.
```sh
$ lcm_spy.sh
```

#### `gen_types.sh`: autogenerate marshalling code for types in the `types` directory
```sh
$ gen_types.sh
```

## IPython
```sh
$ sudo apt-get install ipython-notebook python-dev python-pip # gets dependencies for ipython notebook
$ sudo pip install ipython[notebook] --upgrade  # upgrades ipython notebook to latest version
$ ipython notebook                # runs ipython-notebook
```

## ROS
http://wiki.ros.org/indigo/Installation/Ubuntu
