#!/bin/bash
# run from the previous directory. TODO use any directory
# deploys the repo to the robots.
# You will need to setup a passwordless ssh key to use this.

rsync -avi . bml@192.168.1.140:/home/bml/zumy&
#rsync -avi . bml@192.168.1.121:/home/bml/zumy&
#rsync -avi . bml@192.168.1.122:/home/bml/zumy&
#rsync -avi . bml@192.168.1.123:/home/bml/zumy&
#rsync -avi . bml@192.168.1.124:/home/bml/zumy&
#rsync -avi . bml@192.168.1.125:/home/bml/zumy&
#rsync -avi . bml@192.168.1.126:/home/bml/zumy&
#rsync -avi . bml@192.168.1.128:/home/bml/zumy&
#rsync -avi . bml@192.168.1.129:/home/bml/zumy&
#rsync -avi . bml@192.168.1.140:/home/bml/zumy&