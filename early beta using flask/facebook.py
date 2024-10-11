from flask import *
import requests

from pymessenger import Bot

import openai
import os
import time
import random


verifyToken='open'
# ngrok http 5000

#pip install -Iv openai==0.27.8 , we are using version 0.27.8 of openai

# ADD YOUR OPENAI KEY HERE
 
app = Flask(__name__)

page_acess_token='' # use the facebook developer tools page to get the page_acess_token for your account 

API = "https://graph.facebook.com/LATEST-API-VERSION/me/messages?access_token="+page_acess_token
bot= Bot(page_acess_token)

def runCHatBot(userName):

    allMessages=[] # this array will have all the messages so far with the current user from the bot and the user

    subfolder_path = os.path.join(os.getcwd(), "Existing_Chatlogs")
    file_path = os.path.join(subfolder_path, userName+".txt")

    exsitingChatLogs = open(file_path, "r")
    LinesE = exsitingChatLogs.readlines()

    for line in LinesE: # this loop will add all the chatlogs from the past into our allMessages array
        splitLines=line.split("||")
        if(1 < len(splitLines)): #  added this if
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
        newResponse=str(response).split("|")
        if(newResponse[1] == "True"):
          print("!!!!SCAMMER FOUND!!!!")
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
        userchatlogs.write("role||"+"system||") # the first message has the system role
        userchatlogs.write("content||"+userInput)
        userchatlogs.write("\n")
        userInput=msg
        userchatlogs.write("role||"+"user||")  # all other messages past the first message have the user role

    else: # if there are chatlogs for the current user
        userchatlogs=open(file_path, "a")
        userInput=msg
      # added a /n here 
        userchatlogs.write("\nrole||"+"user||")  # all other messages past the first message have the user role  CHANGED THIS LINE

    userchatlogs.write("content||"+userInput)
    userchatlogs.write("\n")
    userchatlogs.close()


def RunMisSpell(wordToMisSpell): # added this
  allMessagesMis=[]
  prompt= "For the rest of this chat I'm going to type a word and I want you to reply with 5 common ways that people misspell that word"
  tempLogs=""
  allMessagesMis.append({"role": "system", "content": prompt})
  allMessagesMis.append({"role": "system", "content": wordToMisSpell})

  completedResponse=False
  while(completedResponse==False): # sometimes openai times out,so we are gonna keep trying until it does not time out
      try:
          # we use ChatCompletion to get responses from openai
          response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=allMessagesMis)
          completedResponse=True
      except:
          pass

  response= response["choices"][0]["message"]["content"]
  response= response.split("\n")
  returnResponse=[]
  for rep in response: 
    try:
      returnResponse.append(rep.split(".")[1])
    except:
      pass

  try:
    return random.choice(returnResponse).split("(")[0]
  except:
    return wordToMisSpell


def misspellMessage(sentence, prob):
    words = sentence.split()
    misspelled_sentence = []

    for word in words:
        if random.random() < prob:
            # Misspell the word by asking chatgpt common ways that word is mispelled
            # and randomly picking one of the 5 common ways that word is mispelled
            misspelled_word=RunMisSpell(word) # added this
            misspelled_sentence.append(misspelled_word)
        else:
            misspelled_sentence.append(word)

    return ' '.join(misspelled_sentence)


# Create an endpoint in the flask app
def process_message(author_id, msg):

    AuthtorBackend(str(author_id),msg)
    reply = runCHatBot(str(author_id))
    return reply



@app.route("/", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == verifyToken:
            return request.args.get("hub.challenge")
        else:
            return "Not connected to facebook, SAD!"
    elif request.method == "POST": # messages get sent to you
        payload= request.json
        event = payload['entry'][0]['messaging']

        for msg in event:
            text= msg['message']['text']
            senderid = msg['sender']['id']

            response= process_message(senderid,text)
            print("sent",response)
            splitReplies= response.split(".") # remove periods
            for sr in splitReplies:
                newReply=sr

                # we will remove any commas 
                newReply = newReply.replace(",", "")

                # 5 percent chance the message will have some spelling mistake for each word in the sentence
                newReply = misspellMessage(newReply,0.05)

                chanceOfAllCaps=random.randint(1, 100)
                # 15 percent of the time the message will have caps in it
                if(0 < len(newReply) and chanceOfAllCaps <= 15  ):
                    #print("message was",newReply,"length was",len(newReply))
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

                bot.send_text_message(senderid,newReply)
            
        
        return "Message Received"
        
    else:
        return "200"


if __name__ =='__main__':
    app.run()
    



