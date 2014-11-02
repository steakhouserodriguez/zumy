Robot Bringup From Image
========================

# Overview
* Imaging SD card
* Networking
* Set Robot ID
* Test

## Imaging SD Card
http://nbviewer.ipython.org/github/biomimetics/bml_tools/blob/master/arm_linux/odroid_imaging.ipynb

## Networking
* Use a serial terminal to login
* check the device name via `ifconfig -a`
* modify `/etc/network/interfaces` to set the IP address

# Set robot ID
```sh
bml@odroid-server:~$ echo '/040' > ~/zc_id
```

# Test
1. Launch IPython Notebook:
    ```sh
    bml@odroid-server:~$ ipython notebook --ip=* --no-browser
    ```

2. Open http://192.168.1.66:8888, navigate to zumy > notebook > for tests.

