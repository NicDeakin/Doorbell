import time
import os
import uuid
import RPi.GPIO as GPIO
import socket
import subprocess
import signal

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

IP = '10.0.0.153'
port = 5560

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP,port))

def sendMessage(url):
	message = url
	sock.send(str.encode(url))

def createVideoChat(url, meetingProcess):
	
	process = None
	if not meetingProcess:
		process = subprocess.Popen(["chromium-browser", url])
		time.sleep(60)
		os.kill(process.pid, signal.SIGTERM)
	else:
		print("Meeting already started")
	return process
def ring(channel):
	GPIO.remove_event_detect(10)
	chatid = str(uuid.uuid4())
	url = "http://meet.jit.si/%s" % chatid
	meetingProcess = None
	if not meetingProcess:
		print("Meeting Start")
		sendMessage(url)
		meetingProcess = createVideoChat(url, meetingProcess)
		print("Meeting ended")
		meetingProcess = None
	else:
		print("Meeting has already started")
	GPIO.add_event_detect(10,GPIO.RISING,callback=ring)
GPIO.add_event_detect(10,GPIO.RISING,callback=ring, bouncetime = 2000)
while True:
	try:
		time.sleep(0.1)
	except KeyboardInterrupt:
		print("Shutting Down")
		break
