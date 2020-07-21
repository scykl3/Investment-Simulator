import tkinter
from tkinter import *
import numpy

root = tkinter.Tk()
root.title("Investment Simulator")
root.geometry('1000x1080')
root.configure(bg='black')
home = Frame(root,width=1000, height=1080)
market = Frame(root,width=1000, height=1080)
portfolio = Frame(root,width=1000, height=1080)
home.configure(bg = "white")
def raise_frame(frame):
    frame.tkraise() #Brings desired frame to the top
    
for frame in (home, market, portfolio):
    #Set frame to fill page
    frame.configure(bg="green") #Background Color
    frame.grid(sticky='nswe')
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.grid(row=0,column=1)  

    #Page Buttons
    Button(frame, text='Home',fg='black', bg='grey', relief=FLAT, command=lambda:raise_frame(home)).place(x=50,y=50)
    Button(frame, text='Market',fg='black', bg='grey', relief=FLAT, command=lambda:raise_frame(market)).place(x=104,y=50)
    Button(frame, text='Portfolio',fg='black', bg='grey', relief=FLAT, command=lambda:raise_frame(portfolio)).place(x=160,y=50)    
    
#Home Page
balance = "100,000,000"
cur_bal_txt = tkinter.Text(home, height = 2, bg = 'black', fg = 'grey', relief=FLAT)
cur_bal_txt.configure(font=("Calibri", 30, ""))
cur_bal_txt.insert(tkinter.END, "Your Balance:)
cur_bal_txt.insert(tkinter.END, balance)
cur_bal_txt.place(x=100,y=100)
cur_bal_txt.config(state=DISABLED)
 
#Market Page
graph = tkinter.Text(market, bg = 'black', fg = 'grey', relief=FLAT,height=1)
graph.configure(font=("Calibri", 30, ""))
graph.insert(tkinter.END, "How do i graph")
graph.place(x=100,y=400)
graph.config(state=DISABLED)

#Portfolio Page
equity = "100,000,000"
equity_txt = tkinter.Text(portfolio, height=2, bg = 'black', fg = 'grey', relief=FLAT)
equity_txt.configure(font=("Calibri", 30, ""))
equity_txt.insert(tkinter.END, "Your Equity:\n")
equity_txt.insert(tkinter.END, "100,000,000")
equity_txt.place(x=100,y=100)
equity_txt.config(state=DISABLED)


#Launch Porgram
home.tkraise()
root.mainloop()
