import train
import chat

mode = input("Enter your mode 'train' or 'chat': ")

if mode == 'train':
    train.train()
elif mode == 'chat':
    chat.chat()
else:
    print("This mode doesn't exist.") 
