import random
import tkinter as tk
import time as t
from yahoo_fin.stock_info import *
import yfinance as yf
import tkinter.font

keepGoing = True
buyMoney = 10000.0
stockMoney=0
totalMoney = buyMoney
stocks={}

def buyStock():#this function allows the user to buy stocks
    global buyMoney
    global stockMoney
    global totalMoney
    stockPrice = get_live_price(nameField.get())#get the stock price of the wanted stock
    buyMoney = buyMoney -stockPrice*int(numField.get())#makes the transaction
    if str(nameField.get()) in stocks.keys():#stores it in a dictionary
        stocks[nameField.get()][0] +=int(numField.get())
        stocks[nameField.get()][1] =stockPrice
    else:
        stocks[nameField.get()] = [int(numField.get()),stockPrice]
    stockMoney += stockPrice*int(numField.get())
    print(stockPrice)
    currMoney()

    return()

def sellStock(): #this function allows the user to sell stocks
    global buyMoney
    global stockMoney
    global totalMoney
    stockPrice = get_live_price(nameField.get())#get the live price of a stock
    stocks[nameField.get()][1] = stockPrice #update stock price
    buyMoney = buyMoney+stockPrice #updates how much spending money you have
    if stocks[nameField.get()][0] == 1:#updates the stock count/portfolio
        stocks.pop(nameField.get(),None)
    else:
        stocks[nameField.get()][0]-=1
    stockMoney-=stockPrice
    currMoney()
    return()
def currMoney(): # finds how much money with stocks you have
    global totalMoney
    totalMoney = 0.0
    for key, value in stocks.items():#recalculates the total money you have
        value[1] = int(get_live_price(key))
        totalMoney+= value[0]*value[1]
    totalMoney+=buyMoney
    print(totalMoney)
    root.after(60000,currMoney)
    return()
root = tk.Tk()
root.geometry('500x500')
root.configure(bg='black')
frame = tk.Frame(root)
frame.pack()
str_var = tk.StringVar(value=str(totalMoney))
textMoney=tk.Label(root, textvariable=str_var)
textMoney.place(x=200,y=100)
currMoney()
str_var.set(totalMoney)
buy=tk.Button(frame,text="BUY",fg="red",
                 activebackground='blue',
                 command=buyStock)
buy.pack(side=tk.LEFT)
sell=tk.Button(frame,text="SELL",fg="red",
               activebackground='red',
               command=sellStock)
sell.place(x=500,y=500)
sell.pack()
nameField= tk.Entry(root)
nameField.pack()
numField = tk.Entry(root, width=50)
numField.pack()
root.mainloop()