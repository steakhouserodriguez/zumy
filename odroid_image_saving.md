ODROID Image Saving
===================

```bash
user@dev-machine:~$ sudo dd if=/dev/mmcblk0 of=zumy_2014-11-02.img
user@dev-machine:~$ xz zumy_2014-11-02.img
user@dev-machine:~$ md5sum zumy_2014-11-02.img.xz > zumy_2014-11-02.img.xz.md5sum
```
