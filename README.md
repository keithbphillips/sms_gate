# APRS SMS GATE

A flask web application that runs as a service and provides a web page.  Enter a phone number and message and the application drops a message into a folder in which kissutil service processes messages from direwolf connected APRS radio frequency.

Requires: python3+, kissutil, direwolf

- mkdir ~/pi/smsmessages/in
- mkdir ~/pi/smsmessages/out
- cd ~/pi/smsmessages
- git clone https://github.com/keithbphillips/sms_gate.git
- http://localhost:5000
- copy service files to /etc/systemd/system
- systemctl daemon-reload
- systemctl enable kissutil
- systemctl enable smsgate
- systemctl start kissutil
- systemctl start smsgate
- add gen_map.py to crontab */5 * * * *
