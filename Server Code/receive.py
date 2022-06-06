import socket
import subprocess
import signal
import os
import time
import pygame

IP = ""
port = 5560

def setup():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		sock.bind((IP,port))
	except socket.error as msg:
		print(msg)
		sock.close()
	print("Socket binded")
	return sock

def connection(sock):
	sock.listen(1)
	conn, addr = sock.accept()
	print(addr[0])
	print(addr[1])
	return conn

def transfer(conn):
	while True:
		data = conn.recv(1024)
		data = data.decode('utf-8')
		print(data)
		openURL(data)
def openURL(url):
	print("Attempting web")
    
    doorbell = pygame.mixer.Sound("/home/pagen/Desktop/doorbellSound.wav")
    playing = doorbell.play()
    while playing.get_busy():
        pygame.time.delay(100)
        
	process = subprocess.Popen(["chromium-browser", url])
	time.sleep(60)
	os.kill(process.pid,signal.SIGTERM)

sock = setup()
while True:
	try:
		conn = connection(sock)
		transfer(conn)
	except:
		sock.close()
		print("Something went wrong")
		break