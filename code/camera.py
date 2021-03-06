## Made by Tan Mai (nhattanmai91@gmail.com)
## Date: 30-May-2015

import os
import RPi.GPIO as GPIO
import time
import picamera
import datetime 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from subprocess import call  

video_num = 0
sensor = 4

## Setting up work place
def check_dir_exist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

WORKING_DIR = "/home/pi/Desktop/CCTV/"
UPLOADER_DIR = WORKING_DIR + "code/"
UPLOADER_FILE = "dropbox_uploader.sh"
LOCAL_VIDEO_DIR = WORKING_DIR + "video-files/"
DROPBOX_VIDEO_DIR = " ."
LOCAL_LOG_DIR = WORKING_DIR + "logs/"

VIDEO_UPLOAD_CMD = UPLOADER_DIR + UPLOADER_FILE + " upload "

check_dir_exist(WORKING_DIR)
check_dir_exist(UPLOADER_DIR)
check_dir_exist(LOCAL_VIDEO_DIR)
check_dir_exist(LOCAL_LOG_DIR)
## End of Setting up work place

def get_file_name():  
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.h264")

## Emailing
def sendEmail(filename, photos):

    msg = MIMEMultipart()
    TO = 'reciever@gmail.com'
    msg['Subject'] = "Report from Rpi"

    # Gmail Sign In
    gmail_sender = 'sender@gmail.com'
    gmail_passwd = 'password'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    msgBody = "Video file's name: " + filename + ".<br>Please check your Dropbox."
    msgText = MIMEText(msgBody , 'html')
    msg.attach(msgText)

    # Attach any new photos
#    if photos is not None:
#        for photo in photos:
#            
#            fp = open(os.path.join(sys.path[0],photo), 'rb')
#            img = MIMEImage(fp.read())
#            fp.close()
#            img.add_header('Content-ID', '<{}>'.format(str(photo)))
#            msg.attach(img)    
#            
    try:
        server.sendmail(gmail_sender, [TO], msg.as_string() ) #BODY)
        print ('Email is sent.')
        server.quit()
    except:
        print ('Error sending email. Please check your Internet connection')
## End of Emailing

## Logging
def write_log(video_num, video_name, is_upload_success):
    log_file = open(LOCAL_LOG_DIR + datetime.datetime.now().strftime("%Y-%m-%d.log"), "a")
    log_file.write("%d - %s - %s\n" % (video_num, video_name, is_upload_success))
    log_file.close()
## End of Logging

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

cam = picamera.PiCamera()

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"

        if current_state:
            video_num += 1
            print("Recording video number %d...") % video_num

            fileName = get_file_name()
            file_address = LOCAL_VIDEO_DIR + fileName
            video_upload_cmd = VIDEO_UPLOAD_CMD + file_address      #dropbox
            video_upload_cmd += DROPBOX_VIDEO_DIR #dropbox

            cam.start_preview()
            cam.start_recording(file_address)  

	    time.sleep(10)			  #time length of video (in second)

            cam.stop_preview()
            cam.stop_recording()
	    print("Stopped video %d. File name: %s") % (video_num, fileName)
            time.sleep(1)
	    print("Dropboxing...")
            call ([video_upload_cmd], shell=True) #dropbox
	    print("Done Dropboxing")
            write_log(video_num, fileName, "DONE")
            sendEmail(fileName, None);		  #Sending email to notify
	    print("-----------------------------")
