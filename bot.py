from telegram import *
from telegram.ext import * 
import os
from selectorlib import Extractor
import re
import json

print("Bot Started...")

bot = Bot("YourtokenHere")

# print(bot.get_me())

updater = Updater("YourtokenHere",use_context=True)
dispatcher = updater.dispatcher

def start(update:Update, context=CallbackContext):
    # print('json file update : ' ,update)
    # print("json file bot : ', bot)
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    print("chat_id : {} and firstname : {} lastname : {}  username {}". format(chat_id, first_name, last_name , username))
    bot.sendMessage(chat_id, f'Hello {first_name} {last_name} send me message which conatins a link')

def Find(string):
  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]


# This is the main function which sends the message
def msg_function(update:Update, context=CallbackContext):
    y = Find(update.effective_message.text)
    with open("app/urls.txt", "w") as amazonUrls:
        for r in range(0,len(y)):
            amazonUrls.write(y[r]+"\n")
    print(update.effective_message.text)

    try:
        os.system("python app/amazon.py") #Runs amazon scraping script
        os.system("python app/flipkart.py") #Runs flipkart scraping script
    except:
        pass

    amazonData = [] # We are creating the Dictionary to iterating same key data
    with open("app/amazon_output.jsonl") as amazonOutput:
            for AD in amazonOutput:
                amazonDict = json.loads(AD)
                amazonData.append(amazonDict)
            
            amazonImageUrls =[] #This will get a list of images url with the same key "images"
            for IU in amazonData:
                amazonImages = IU["images"]
                amazonImageUrls.append(amazonImages)
            
            amazonList = amazonImageUrls #lets save our list in variable
    
    flipkartData = [] # We are creating the Dictionary to iterating same key data
    with open("app/flipkart_output.json") as flipkartOutput:
            for FD in flipkartOutput:
                flipkartDict = json.loads(FD)
                flipkartData.append(flipkartDict)
            
            flipkartImageUrls =[] #This will get a list of images url with the same key "images"
            for IU in flipkartData:
                flipkartImages = IU["images"]
                flipkartImageUrls.append(flipkartImages)
            
            flipkartList = flipkartImageUrls #lets save our list in variable
    
    list = amazonList + flipkartList
    print(list)
    try: #sends message if all input is correct
        bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(list[0],caption=update.effective_message.text)] +[InputMediaPhoto(list[i]) for i in range(1, len(list))]
            )
    
    except: #error handler
        bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.effective_message.text
        )

def contact(update:Update, context=CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Want to ask something? Contact @Arpit_goyall'
        )
        
# cmd_handler = CommandHandler('settings', settings)
contact_cmd_handler = CommandHandler('contact', contact)
start_cmd_handler = CommandHandler('start', start)
msg_handler = MessageHandler(Filters.text, msg_function)



# dispatcher.add_handler(cmd_handler)
dispatcher.add_handler(contact_cmd_handler)
dispatcher.add_handler(start_cmd_handler)
dispatcher.add_handler(count_cmd_handler)
dispatcher.add_handler(msg_handler)


updater.start_polling()
