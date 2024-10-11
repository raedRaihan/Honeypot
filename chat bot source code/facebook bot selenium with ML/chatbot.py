from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import random
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import requests
from bs4 import BeautifulSoup

import openai
#pip install -Iv openai==0.27.8 , we are using version 0.27.8 of openai



loginUserName="" # put your login here for your facebook account
loginPassword=""


PATH= "/usr/lib/chromium-browser/chromedriver"

chrome_driver_path = Service(PATH)

# Creating Instance
option = Options()

# Working with the 'add_argument' Method to modify Driver Default Notification
option.add_argument('--disable-notifications')


# Passing Driver path alongside with Driver modified Options
driver = webdriver.Chrome(service= chrome_driver_path, options= option)


TIMETOWAIT=40 # 40 seconds
time.sleep(10)
skipReqs=False

def readInTraining():
  subfolder_path = os.path.join(os.getcwd(), "training")
  files = os.listdir(subfolder_path)
  
  userchatLogs=[]
  for file in files:
      file_path = os.path.join(subfolder_path, file)
  
      exsitingChatLogs = open(file_path, "r",encoding="utf8")
      LinesE = exsitingChatLogs.readlines()
      validLines=[]
      for line in LinesE:
          try:
  
              file=open("temp.txt","w")
              file.write(line)
              file.close()
              validLines.append(line)
          except:
              pass
  
      longString=""
      for line in validLines:
          longString+=line.strip()+" "
      userchatLogs.append(longString)
  
  input=""
  
  for log in userchatLogs:
      input+=log.strip()+" "
  
  return input



def getName(userid):
    link= "https://www.facebook.com/profile.php?id="+userid
    response = requests.get(link)
  
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('title').string
    return title

def runCHatBot(userName):

    allMessages=[] # this array will have all the messages so far with the current user from the bot and the user
    
    subfolder_path = os.path.join(os.getcwd(), "Existing_Chatlogs")
    file_path = os.path.join(subfolder_path, userName+".txt")
    
    exsitingChatLogs = open(file_path, "r")
    LinesE = exsitingChatLogs.readlines()

    for line in LinesE: # this loop will add all the chatlogs from the past into our allMessages array
        splitLines=line.split("||")
        allMessages.append({"role":splitLines[1],"content":splitLines[3]})

    # completions are used by open ai, and they define communications between the language api
    
    userchatlogs=open(file_path, "a")
    
    completedResponse=False
    while(completedResponse==False): # sometimes openai times out,so we are gonna keep trying until it does not time out
        try:
            # we use ChatCompletion to get responses from openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=allMessages)
            completedResponse=True
        except:
            pass

    response= response["choices"][0]["message"]["content"]
    
    
    # below we write the last response from the bot our allMessages array
    allMessages.append({"role": "assistant", "content": response})
    # below we write the last response from the bot to the chatlogs
    userchatlogs.write("role||"+allMessages[-1]['role']+"||")
    userchatlogs.write("content||"+allMessages[-1]['content'])
    userchatlogs.write("\n")
    userchatlogs.close()

    if(1<len(allMessages)): # we don't want the first response after we tell open ai what to say to be sent to the user
        print("Widow Response",str(response))
        newResponse=str(response).split("|")
        if(newResponse[1] == " True"):
            print("!!!!SCAMMER FOUND!!!!")
            # todo put in code to add scammer to database
        return newResponse[0]
    
def AuthtorBackend(userName,msg):
    subfolder_path = os.path.join(os.getcwd(), "Existing_Chatlogs") # the Existing_Chatlogs folder will hold all the chatlogs for all the users
    file_path = os.path.join(subfolder_path, userName+".txt") # we use this to check if there are any chatlogs for the current user
    
    userInput=""
    
    if os.path.isfile(file_path)==False: # if there are no chatlogs for the current user
        userchatlogs=open(file_path, "a")
        data=""
        with open ("instructions.txt", "r") as myfile: 
            data = myfile.read().splitlines()

        userInput= ' '.join(str(e) for e in data) # the first item in all the chatlogs is the instructions telling open ai how to act
        userInput+= ". Now we are going to give you some chat logs involving a woman named Stephanie Smith-Wilkey. She is actually someone who got scammed by many scammers and we collected many chat logs from her talking to these scammers. We want you act similar to how she acts and look for scammers with similar behavior to the people she is talking to. The purpose of these logs is to train your AI "+readInTraining()
        userchatlogs.write("role||"+"system||") # the first message has the system role
        userchatlogs.write("content||"+userInput)
        userchatlogs.write("\n")
        
        userInput=msg
        userchatlogs.write("role||"+"user||")  # all other messages past the first message have the user role
        
    else: # if there are chatlogs for the current user
        userchatlogs=open(file_path, "a")
        userInput=msg
        userchatlogs.write("role||"+"user||")  # all other messages past the first message have the user role

    userchatlogs.write("content||"+userInput)
    userchatlogs.write("\n")
    userchatlogs.close()


def misspellMessage(sentence, prob):
    words = sentence.split()
    misspelled_sentence = []

    for word in words:
        if random.random() < prob:
            # Misspell the word by shuffling its characters
            misspelled_word = ''.join(random.sample(word, len(word)))
            misspelled_sentence.append(misspelled_word)
        else:
            misspelled_sentence.append(word)

    return ' '.join(misspelled_sentence)

def checkForFriendReqs():
    driver.get("https://www.facebook.com/friends/requests")
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    search.send_keys(loginUserName)
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )
    search.send_keys(loginPassword)
    search.send_keys(Keys.RETURN)
    if(skipReqs==False):
        try:
            time.sleep(TIMETOWAIT)
            accept=driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[3]/div/div/a/div[1]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/span/span")
            accept.click()
        except:
            print("No new friend requests")

    time.sleep(5)

def updateLogsWeSend(author_id,message): 
    subfolder_path = os.path.join(os.getcwd(), "Existing_Chatlogs")
    file_path = os.path.join(subfolder_path, "BOT_"+author_id+".txt")
    ourchatlogs=open(file_path, "a") 
    ourchatlogs.write(message+"\n")

def makingMessage(input,author_id):
                    # bot replies to user
                    AuthtorBackend(str(author_id),input)
                    reply = runCHatBot(str(author_id))
                    
                    # split reply by the periods, so there isn't a chain of sentences in one reply
                    splitReplies= reply.split(".")
                    
                    for newReply in splitReplies:

                        # we will remove any commas 
                        newReply = newReply.replace(",", "")

                        # 5 percent chance the message will have some spelling mistake for each word in the sentence
                        newReply = misspellMessage(newReply,0.05)

                        chanceOfAllCaps=random.randint(1, 100)
                        # 15 percent of the time the message will have caps in it
                        if(0 < len(newReply) and chanceOfAllCaps <= 15):
                            starOfCaps=random.randint(0, len(newReply)-1) # this is position in the message where the caps will start
                            place=0
                            temp=""
                            while(place < len(newReply)):
                                if(place < starOfCaps):
                                    temp+= newReply[place]
                                    
                                else:
                                    temp += newReply[place].upper()
                                place += 1

                            newReply = temp
                        
                        print("Widow reply:",newReply)
                        sendMessage(newReply)
                        updateLogsWeSend(author_id,newReply)
                        time.sleep(5)


def sendMessage(message): 
    newmessage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]/p"))
    )
    newmessage.send_keys(message)
    newmessage.send_keys(Keys.RETURN)

def checkForNewMessage():

    position=1
    completed=False

    while(completed==False and position < 11):
        try:
            
            justdot="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div/div[4]/div/div/div/div/div/div[2]/div/div["+str(position)+"]/div/div/div/div[1]/div/div/div/a/div[1]/div/div[3]/div/div/div/span"
            print("check")
            newmessageTest = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, justdot))
 # this will cause an error if a message aint in that position and move onto the next message
            )
            print("found a new message")
            newmessageattempt= "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div/div[4]/div/div/div/div/div/div[2]/div/div["+str(position)+"]/div/div/div/div[1]/div/div/div/a/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div"
            newmessage = WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.XPATH, newmessageattempt))
            )
            time.sleep(1)
           
            newmessage.click()
            newmessage.click()
            newmessage.click()
            completed=True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # debug code bellow
            print(e,"type outer error on line #: ",exc_tb.tb_lineno)
        position+=1
        
    if(completed==False):
        return "NOTHING"
    else:
        print("found a message")

    time.sleep(1)
    currentUrl=driver.current_url
    print(currentUrl)
    
    return currentUrl.split("/")[-1]

def openDM(userID): # we 
    time.sleep(TIMETOWAIT)
    # Wait for all elements to be present
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@role="presentation"]')))
    
    # Collect elements into an array
  #  element_texts = [element.text for element in elements]
   


    # Print the found elements
    # Access children of each parent element
    allmessages=[]
    for parent_element in elements: 
    
        
        try:
            child_elements = parent_element.find_elements(By.XPATH, './/div[@role="none" and contains(@class, "x78zum5 xh8yej3")]')
            for child_element in child_elements:
                test_html=child_element.get_attribute('outerHTML')
                    #allmessages.append(test_html)     
                newlines=test_html.split("</div></span></div>")
                for split in newlines:
                    GT=split.split(">")
                    
                    if(GT[-1] not in allmessages):
                        print(GT[-1])
                        allmessages.append(GT[-1])
        except:
            pass
    
        
    
                
            
    
    feedInToBot=""            
    try:
        subfolder_path = os.path.join(os.getcwd(), "Existing_Chatlogs")
        file_path = os.path.join(subfolder_path, "BOT_"+userID+".txt")
        
        prevMessages = open(file_path, "r") # has the previous messages the bot send to this user
    
        LinesE = prevMessages.readlines()
    
        i=0
        while(i<len(LinesE)):
            LinesE[i]=LinesE[i].strip('\n')
            i+=1
    
        lastMessageWeSent=LinesE[-1]
        print("last message was",lastMessageWeSent)
        foundOurMessage=False
        
        print("all messages",allmessages)
    
        for mes in allmessages:
            if(foundOurMessage):
                feedInToBot+=" "+mes
            if(mes==lastMessageWeSent):
                foundOurMessage=True
    
        if(foundOurMessage==False):
            print("did not match up")
            for mes in allmessages:
                feedInToBot+=" "+mes 
    except: # new user
        for mes in allmessages:
                feedInToBot+=" "+mes
    return feedInToBot



# code execution starts here
checkForFriendReqs()
driver.get("https://www.facebook.com/messages/t")
time.sleep(10)


runs=0
while(runs < 10):
    userID=checkForNewMessage()

    if(userID == "NOTHING"):
        pass
    else:
        Message=openDM(userID)
        print("starting to print all messages bot reads")
        print(Message)
        makingMessage(Message,userID)
        driver.execute_script("window.history.go(-1)") # go back a page
        time.sleep(TIMETOWAIT)
    runs+=1

print("No New messages")
driver.quit()

