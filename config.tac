root% twistd -ny finger.tac # just like before
root% twistd -y finger.tac # daemonize, keep pid in twistd.pid
root% twistd -y finger.tac --pidfile=finger.pid
root% twistd -y finger.tac --rundir=/
root% twistd -y finger.tac --chroot=/var
root% twistd -y finger.tac -l /var/log/finger.log
root% twistd -y finger.tac --syslog # just log to syslog
root% twistd -y finger.tac --syslog --prefix=twistedfinger # use given prefix
