import time
import subprocess

timeInBetweenDMCheck=21600
timeInBetweenPost=0
print("starting")
while True:
    time.sleep(timeInBetweenDMCheck)
    timeInBetweenPost+=6
    if(timeInBetweenPost>24): # whole day passed so we make a post
        timeInBetweenPost=0
        subprocess.call("/home/pi/Python-3.9.15/python facebook_posts.py 1", shell=True)
    else: # we check our dms and friend requests 
        pass
        subprocess.call("/home/pi/Python-3.9.15/python chatbot.py 1", shell=True)