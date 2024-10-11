import os
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


import openai

 # ADD YOUR OPENAI KEY HERE






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

def adderror(message):
    newReply=message
    # we will remove any commas 
    newReply = newReply.replace(",", "")

    # 2 percent chance the message will have some spelling mistake for each word in the sentence
    newReply = misspellMessage(newReply,0.02)

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

    return newReply

def runBot():
    allPosts=[]

    prevmessages=open("prevPosts.txt", "a")

    prevmessages.write("\nrole||"+"user||")
    prevmessages.write("content||"+"+")
    prevmessages.write("\n")
    prevmessages.close()

    prevmessages=open("prevPosts.txt", "r")

    LinesE = prevmessages.readlines()

    for line in LinesE: # this loop will add all the chatlogs from the past into our allMessages array
        splitLines=line.split("||")
        if(1 < len(splitLines)): #  added this if
          allPosts.append({"role":splitLines[1],"content":splitLines[3]})

    prevmessages.close()
    prevmessages=open("prevPosts.txt", "a")

    completedResponse=False
    while(completedResponse==False): # sometimes openai times out,so we are gonna keep trying until it does not time out
        try:
            # we use ChatCompletion to get responses from openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=allPosts)
            completedResponse=True
        except:
            pass

    response= response["choices"][0]["message"]["content"]

    # below we write the last response from the bot our allMessages array
    allPosts.append({"role": "assistant", "content": response})
    # below we write the last response from the bot to the chatlogs
    prevmessages.write("role||"+allPosts[-1]['role']+"||")
    prevmessages.write("content||"+allPosts[-1]['content'])
    prevmessages.write("\n")
    prevmessages.close()
    return response


if os.path.isfile("prevPosts.txt")==False: # if there are no previous messages
    data=""
    with open ("Inst_for_posts.txt", "r") as myfile:
        
        prevmessages=open("prevPosts.txt", "a")
        data = myfile.read().splitlines()

        firstMessage= ' '.join(str(e) for e in data) # the first item in all the chatlogs is the instructions telling open ai how to act
        prevmessages.write("role||"+"system||") # the first message has the system role
        prevmessages.write("content||"+firstMessage)



newMessage=runBot()
newMessage=adderror(newMessage)





PATH= "/usr/lib/chromium-browser/chromedriver"

chrome_driver_path = Service(PATH)

# Creating Instance
option = Options()

# Working with the 'add_argument' Method to modify Driver Default Notification
option.add_argument('--disable-notifications')


# Passing Driver path alongside with Driver modified Options
driver = webdriver.Chrome(service= chrome_driver_path, options= option)

#chrome_driver_path = Service(PATH)
#driver = webdriver.Chrome(service=chrome_driver_path)
time.sleep(10)




driver.get("https://www.facebook.com/messages/t")

search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "email"))
)


search.send_keys("honeypot4316@gmail.com")
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "pass"))
)
search.send_keys("Dummy@account1")
search.send_keys(Keys.RETURN)


driver.execute_script("window.open('');") 
driver.switch_to.window(driver.window_handles[1]) 
driver.get("https://www.facebook.com/profile.php?id=61552331525670")


post_message_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[1]/div/div/div/div/div[1]/div"))
)
post_message_button.click()


message = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div[1]"))
)

message.send_keys(newMessage)

post_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[3]/div[2]/div/div"))
)
post_button.click()


time.sleep(10)
driver.quit()