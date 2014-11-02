ODROID Image Writing
===================

Downloaded images from: http://odroid.in/ubuntu_14.04lts/

```bash
user@dev-machine:~$ wget http://odroid.in/ubuntu_14.04lts/ubuntu-14.04lts-server-odroid-u-20140604.img.xz
user@dev-machine:~$ wget http://odroid.in/ubuntu_14.04lts/ubuntu-14.04lts-server-odroid-u-20140604.img.xz.md5sum
user@dev-machine:~$ md5sum ubuntu-14.04lts-server-odroid-u-20140604.img.xz
user@dev-machine:~$ cat disk_images/ubuntu-14.04lts-server-odroid-u-20140604.img.xz.md5sum
user@dev-machine:~$ xzcat ubuntu-14.04lts-server-odroid-u-20140604.img.xz | sudo dd of=/dev/mmcblk0 bs=4M
user@dev-machine:~$ sync
```
