Made by Tan Mai (nhattanmai91@gmail.com)
Date: 30-May-2015
----------------------------
New home CCTV for security issues. It takes a 10s video and then puts this to my dropbox as well as shoots me an email when someone appears. Cool!! But need to do a lots more to make it becomes a commercial product.

Diagram:

PIR --GPIO 4-- RPi---Internet interface (wifi, Ethernet)
                |
                |
              Camera

Usage:
1. 'code' folder has to be in "home/pi/Desktop/CCTV/" folder
2. Open 'camera.py' file, edit Email Sender's info Reciever's info
3. Run code:
   cd code
   sudo python camera.py

- First time you run this code, you need to setup a dropbox. The program will show you how
