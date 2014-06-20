#!/bin/bash
# run from the previous directory. TODO use any directory
# deploys the repo to the robots.

rsync -avi . odroid@192.168.1.120:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.121:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.122:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.123:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.124:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.125:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.126:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.127:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.128:/home/odroid/zumocrawler&
rsync -avi . odroid@192.168.1.129:/home/odroid/zumocrawler&