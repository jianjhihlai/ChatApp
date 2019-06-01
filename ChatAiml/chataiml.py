import aiml
import sys
import os
import glob

mybot_path = './aimldata'
#切換到語料庫所在工作目錄
os.chdir(mybot_path)

mybot = aiml.Kernel()
files = glob.glob('*.aiml')
for learn_file in files:
    mybot.learn(learn_file)
init = True
while True:
    if init:
        message = input("Bot：你好，我可以陪你聊天\n你：")
        init = False
    else:
        message = input("你：")
    if message == "聊天結束":
        break
    else:
        bot_response = "Bot："+mybot.respond(message)+"\n"
    print(bot_response)
