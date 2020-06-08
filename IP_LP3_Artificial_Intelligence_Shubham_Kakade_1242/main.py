from chatterbot import ChatBot
from tkinter import *
from chatterbot.trainers import ListTrainer
import os
bot = ChatBot("My Bot")

trainer = ListTrainer(bot)

for files in os.listdir('mytraining'):
    data = open("mytraining/Data.yml","r",encoding='utf-8').readlines()
    trainer.train(data)

main = Tk()

main.geometry("500x650")

main.title("CloudCounselage ChatBot")
img = PhotoImage(file="CloudCounselageLogo.png")
photoL = Label(main, image=img)

photoL.pack(pady=3)


def ask_from_bot() :
    query = textF.get()
    answer_from_bot = bot.get_response(query)
    msgs.insert(END, "you : " + query)
    msgs.insert(END, "Bot : " + str(answer_from_bot))
    textF.delete(0, END)
    msgs.yview(END)


frame = Frame(main)

sc = Scrollbar(frame, orient=VERTICAL)
sc1 = Scrollbar(frame, orient=HORIZONTAL)
sc1.pack(side=BOTTOM, fill=X)
msgs = Listbox(frame, width=180, height=20, yscrollcommand=sc.set, xscrollcommand=sc1.set)
sc.pack(side=RIGHT, fill=Y)
sc1.config(command =msgs.xview)

msgs.pack(side=LEFT, fill=BOTH, pady=10)
msgs.insert(END, "Bot :How i can i Help you Today? " )
frame.pack()

textF = Entry(main, font=("Verdana", 15))
textF.pack(fill=X, pady=10)

btn = Button(main, text="Ask", font=("Verdana", 20), command=ask_from_bot)
btn.pack()
main.mainloop()