#Tkinter libraries
import tkinter
from tkinter import *
from tkinter import ttk
#Matplot/graphing libraries
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
#Misc libraries
from collections import Counter 
import yfinance as yf
from yahoo_fin.stock_info import *

root = tkinter.Tk()
root.title("Investment Simulator")
root.geometry('1280x700')
root.configure(bg='black')
home = Frame(root,width=1280, height=700)
watchlist = Frame(root,width=1280, height=700)
market = Frame(root,width=1280, height=700)
portfolio = Frame(root,width=1280, height=700)
graphing = Frame(root,width=1280, height=700)

#Grabbing Data
photo = PhotoImage(file = r"C:\Users\alexa\Downloads\Code\NWAPW\mag_glass.png")
photo = photo.subsample(15,15) 
datafile = open(r"C:\Users\alexa\Downloads\Code\NWAPW\data.txt").read().split()
wlist = eval(datafile[0])#current watchlist
invested_before = eval(datafile[1])  #The day before? depends... you choose what data to put
shares = eval(datafile[2])
prices = dict()
names = dict()
for index in wlist:
    print(index)
    prices[index] = get_live_price(index)
    stock = yf.Ticker(index)
    names[index] = stock.info['shortName']


global wlist_index
wlist_index = 0
def raise_frame(frame):
    frame.tkraise() #Brings desired frame to the top
def on_change(*args):
    value = var_text.get()
    value = value.strip().lower()
    if value == '':# get data from test_list
        data = test_list
    else:
        data = []
        for item in test_list:
            if value in item.lower():
                data.append(item)    
    listbox_update(data)# update data in listbox
def listbox_update(enter):
    name = list()
    if enter != [] and enter != '':
        query = enter
        print('a',query)
        response = requests.get("https://ticker-2e1ica8b9.now.sh/keyword/"+query)
        data = response.text.split(',')
    
        for index in range(0, len(data), 2):
            data[index] = data[index].split(':')
            name.append(data[index][1].replace('"',''))
            listbox.insert('end', data[index][1].replace('"',''))
        print(enter,'a',name)
    return name
def on_select(event):
    try:
        graph_page(event.widget.get(event.widget.curselection()))
    except:pass
for frame in (watchlist, market, portfolio, graphing, home):
    #Set frame to fill page
    frame.configure(bg="black") #Background Color
    frame.grid(row=0,column=0,sticky="nsew")
    #Page Buttons
    global test_list
    test_list = ''
    var_text = StringVar()
    var_text.trace('w', on_change)
    butt = Button(frame, text='Find')
    entry = Entry(frame, textvariable=var_text)
    entry.place(relx=0.7,y=50)
    butt.place(relx=0.67,y=50)
    listbox = Listbox(frame, height = 2)
    listbox.place(relx=0.7,y=65)
    listbox_update(entry.get())
    test_list = listbox_update(entry.get())
    butt.config(command = lambda:[listbox_update(entry.get()),listbox.bind('<<ListboxSelect>>', on_select)])
    Button(frame, text='Home',font=("Calibri", 25, ""),fg='black', bg='grey', relief=FLAT, command=lambda:raise_frame(home)).place(x=50,y=20)
    Button(frame, text='Market',font=("Calibri", 25, ""),fg='black', bg='grey', relief=FLAT, command=lambda:raise_frame(market)).place(x=180,y=20)    
    Button(frame, text='Portfolio',font=("Calibri", 25, ""),fg='black', bg='grey', relief=FLAT, command=lambda:raise_frame(portfolio)).place(x=330,y=20)
    
def xlabel(x):
    if x==daytime:
        return "5 minutes"
    if x==weektime:
        return "1 hour"
    else:
        return "1 day"
def grapher(x,y,name):
    try:
        canvas.delete('all')
    except:
        pass
    fig = Figure(figsize=(5,5))#increase to make plot bigger
    a = fig.add_subplot(111)#scale??? bigger the number, the smaller the size
    a.plot(x,y,color='blue')
    a.set_title (name+" price", fontsize=16)
    a.set_ylabel("price", fontsize=14)
    a.set_xlabel(xlabel(x), fontsize=14)
    canvas = FigureCanvasTkAgg(fig, master=graphing)
    canvas.get_tk_widget().place(x=100,y=100)
    canvas.draw()
    
def graph_page(name):   #EDIT GRAPH HERE 
    raise_frame(graphing)#Keep this here
    #Edit everything after this line  (make sure the frame name is graphing, not root/master/self/frame .....)
    global weektime
    global yeartime
    global daytime
    nflx = yf.Ticker(name)
    nflx.info
    yearpricelist=list()
    for i in nflx.history(period="1y",interval="1d")["Close"]:
        yearpricelist.append(i)
    yearprice= np.array(yearpricelist)
    daypricelist=list()
    for i in nflx.history(period="1d",interval="5m")["Close"]:
        daypricelist.append(i)
    dayprice= np.array(daypricelist)
    weekpricelist=list()
    for i in nflx.history(period="5d",interval= "1h")["Close"]:
        weekpricelist.append(i)

    weekprice= np.array(weekpricelist)
    weektime=list(range(0,len(weekpricelist)))
    yeartime=list(range(0,len(yearpricelist)))
    daytime=list(range(0,len(daypricelist)))
    Button(graphing, text='Past day',fg='black', bg='grey', relief=FLAT, command=lambda:grapher(daytime,dayprice,name)).place(x=0,y=0)
    Button(graphing, text='Past 5 days',fg='black', bg='grey', relief=FLAT, command=lambda:grapher(weektime,weekprice,name)).place(x=100,y=0) 
    Button(graphing, text='Past year',fg='black', bg='grey', relief=FLAT, command=lambda:grapher(yeartime,yearprice,name)).place(x=200,y=0) 
    
if True:#Home Page
        #Balance
    prev_bal  = int(datafile[4])
    balance = int(datafile[3])
    cur_bal_txt = tkinter.Text(home, height = 3, bg = 'black', fg = 'grey', relief=FLAT)
    cur_bal_txt.configure(font=("Calibri", 30, ""))
    cur_bal_txt.insert(tkinter.END, "Your Balance:\n")
    cur_bal_txt.insert(tkinter.END, '$' + str(balance))
    cur_bal_txt.tag_add("start", "2.0", "3.0")#select tag indexes (lines 2-3)
    cur_bal_txt.tag_config("start", background="black", foreground="white",font=("Calibri", 40, "bold"))#change tag to white
    cur_bal_txt.place(x=100,y=100)
    cur_bal_txt.config(state=DISABLED)#No Editing text box
        #Balance with stocks
    bal_stocks = int(datafile[5])
    bal_stocks_txt = tkinter.Text(home, height = 3, bg = 'black', fg = 'grey', relief=FLAT)
    bal_stocks_txt.configure(font=("Calibri", 30, ""))
    bal_stocks_txt.insert(tkinter.END, "With Stocks: \n")
    bal_stocks_txt.insert(tkinter.END, '$' + str(bal_stocks))
    bal_stocks_txt.tag_add("start", "2.0", "3.0")
    bal_stocks_txt.tag_config("start", background="black", foreground="white",font=("Calibri", 40, "bold"))
    bal_stocks_txt.place(x=500,y=100)
    bal_stocks_txt.config(state=DISABLED)
            #Bal Increase Today
    inc_num = balance - prev_bal
    today = tkinter.Text(home, height = 3, width = len(str(inc_num)), bg = 'black', fg = 'grey', relief=FLAT)
    today.configure(font=("Calibri", 30, ""))
    today.insert(tkinter.END, "Today:\n")
    today.insert(tkinter.END, ' +' + str(inc_num))
    today.tag_add("start", "2.0", "3.0")
    today.tag_config("start", background="#32CD32", foreground="white",font=("Calibri", 20, "bold"))
    today.place(x=900,y=100)
    today.config(state=DISABLED)

        #Watchlist(Home)
    watchlist_txt = tkinter.Text(home, height = 1, width = len("Priority Watchlist:"), bg = 'black', fg = 'white', relief=FLAT)
    watchlist_txt.configure(font=("Calibri", 30, ""))
    watchlist_txt.insert(tkinter.END, "Priority Watchlist:")
    watchlist_txt.place(relx=0.5, y=250, anchor=CENTER)
    watchlist_txt.config(state=DISABLED)
    k = Counter(invested_before) 
    highest = k.most_common(3) # Finding 3 highest values 
    x_coor=0
    scroll_y = tkinter.Scrollbar(home, orient="vertical")
    scroll_y.configure(bg='black')
    index = 0
    # Show price of stock, profit in %, how many shares
    for set in highest:
        Button(scroll_y, bg="white", relief=FLAT, command=lambda set=set:graph_page(set[0]),text = (set[0]+"\n$"+str(round(prices[set[0]],2)) +"   "  + str(round(shares[set[0]]*prices[set[0]] - invested_before[set[0]],2)) + "\n" + names[set[0]])).pack(side='right',expand=True)
        x_coor += len(set[0]+"\n$"+str(set[1]) +"   "  + str(round(set[1] - invested_before[set[0]],2)) + "\n" + names[set[0]]) * 4
    scroll_y.configure()
    scroll_y.place(relx=0.485, y=330, anchor=CENTER)
    
        #Edit
    more = tkinter.Button(home, text="View All",relief=FLAT, width = 6, command = lambda:raise_frame(watchlist))
    more.place(relx=0.485, y=285, anchor = CENTER)

if True:#Watchlist
    wlist_txt = tkinter.Text(watchlist, height = 1, width = len("Watchlist:"), bg = 'black', fg = 'white', relief=FLAT)
    wlist_txt.configure(font=("Calibri", 30, ""))
    wlist_txt.insert(tkinter.END, "Watchlist:")
    wlist_txt.place(x=100,y=100)
    wlist_txt.config(state=DISABLED)
    for frame in (watchlist, portfolio):
        frame_canvas = Frame(frame)# Create a frame for the canvas with non-zero row&column weights
        frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')#plot grid
        frame_canvas.grid_rowconfigure(0, weight=1)#set size
        frame_canvas.grid_columnconfigure(0, weight=1)
        frame_canvas.grid_propagate(False)# Set grid_propagate to False to allow 5-by-5 buttons resizing later
        canvas = Canvas(frame_canvas, bg="white")# Add a canvas in that frame
        canvas.grid(row=0, column=0, sticky="news")#"news" means north,east,west,south  ... covers the entire canvas
        vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)# Link a scrollbar to the canvas
        vsb.grid(row=0, column=1, sticky='ns')#covers from top to bottom (the scroll bar)
        canvas.configure(yscrollcommand=vsb.set)#link scrollbar to canvas
        frame_buttons = Frame(canvas, bg="white")# Create a frame to contain the buttons
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
        rows = 10# Add buttons to the frame
        columns = 10
        index=0
        buttons = [[Button() for j in range(columns)] for i in range(rows)]#creating the empty slots
        for i in range(0, rows):
            for j in range(0, columns):
                try:
                        #name, ticker
                        #share price x amount of shares
                        #profit amount profit %
                    #filling the slots in
                    if frame == portfolio:
                        buttons[i][j] = Button(frame_buttons, bg='white',
                           relief=FLAT,
                           command=lambda index=index:watchlist_page(wlist[index]),
                           text=(wlist[index]+"\n$"+
                                 str(round(prices[wlist[index]],2)) + " x "  +
                                 str(shares[wlist[index]])+'\n' +
                                 str(round(get_live_price(wlist[index])
                                                  - invested_before[wlist[index]],2)) +
                                 ' (' +str(round(get_live_price(wlist[index])/
                                                 invested_before[wlist[index]],2))+
                                 '%)' + "\n" + names[wlist[index]]))
                    else:
                        buttons[i][j] = Button(frame_buttons, bg='white',
                                       relief=FLAT,
                                       command=lambda index=index:watchlist_page(wlist[index]),
                                       text=(wlist[index]+"\n$"+
                                             str(round(prices[wlist[index]],2)) + " x "  +
                                             str(shares[wlist[index]])+'\n' +
                                             str(round(get_live_price(wlist[index])
                                                              - invested_before[wlist[index]],2)) +
                                             ' (' +str(round(get_live_price(wlist[index])/
                                                             invested_before[wlist[index]],2))+
                                             '%)' + "\n" + names[wlist[index]]))
                    buttons[i][j].grid(row=i, column=j, sticky='news')
                    index += 1
                except:
                    #once the index is invalid/wlist is out of items, break loop because all slots are filled
                    break
                
        frame_buttons.update_idletasks()# Update buttons frames idle tasks to let tkinter calculate buttons sizes
        first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, columns)])# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, rows)])
        frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                            height=first5rows_height)
        canvas.config(scrollregion=canvas.bbox("all"))# Set the canvas scrolling region
        if frame == portfolio:
            frame_canvas.place(x=100,y=250)#plot
        else:frame_canvas.place(x=100,y=150)
   
   
#Market Page
graph = tkinter.Text(market, bg = 'black', fg = 'grey', relief=FLAT,height=1)
def year(ticker):
    ticker = yf.Ticker(ticker)
    ticker.info
    yearpricelist=list()
    for f, b in zip(ticker.history(period="1y",interval="1d")["Open"], ticker.history(period="1y",interval="1d")["Close"]):
        yearpricelist.append( 100 * (b - f) / f)
    yearprice= np.array(yearpricelist)
    yeartime=list(range(0,len(yearpricelist)))
    return (yeartime,yearprice)
    
def day(ticker):
    ticker = yf.Ticker(ticker)
    ticker.info
    daypricelist=list()
    for f, b in zip(ticker.history(period="1d",interval="5m")["Open"], ticker.history(period="1d",interval="5m")["Close"]):
        daypricelist.append( 100 * (b - f) / f)
    dayprice= np.array(daypricelist)
    daytime=list(range(0,len(daypricelist)))
    return (daytime,dayprice)
    
def week(ticker):
    weekpricelist=list()
    ticker = yf.Ticker(ticker)
    ticker.info
    for f, b in zip(ticker.history(period="5d",interval= "1h")["Open"], ticker.history(period="5d",interval= "1h")["Close"]):
        weekpricelist.append( 100 * (b - f) / f)
    weekprice= np.array(weekpricelist)
    weektime=list(range(0,len(weekpricelist)))
    return (weektime,weekprice)
    
fig = Figure(figsize=(6,6))#increase to make plot bigger
a = fig.add_subplot(111)#scale??? bigger the number, the smaller the size
def weekgraph():
    try:
        canvas.delete('all')
    except:
        pass
    a.plot(week('NDAQ')[0],week('^IXIC')[1],color='#E5CFAD')
    a.plot(week('^DJI')[0],week('^DJI')[1],color='#D392A4')
    a.plot(week('^GSPC')[0],week('^GSPC')[1],color='#98B7C3')
    a.set_facecolor('black')
    a.set_title ("Market", fontsize=16)
    a.set_ylabel("Price", fontsize=14)
    a.set_xlabel("Day", fontsize=14)  
    canvas = FigureCanvasTkAgg(fig, master=market)
    canvas.get_tk_widget().place(x=100,y=100)
    canvas.draw()

def yeargraph():
    try:
        canvas.delete('all')
    except:
        pass
    a.plot(year('NDAQ')[0],year('^IXIC')[1],color='#E5CFAD')
    a.plot(year('^DJI')[0],year('^DJI')[1],color='#D392A4')
    a.plot(year('^GSPC')[0],year('^GSPC')[1],color='#98B7C3')
    a.set_facecolor('black')
    a.set_title ("Market", fontsize=16)
    a.set_ylabel("Price", fontsize=14)
    a.set_xlabel("Hour", fontsize=14)  
    canvas = FigureCanvasTkAgg(fig, master=market)
    canvas.get_tk_widget().place(x=100,y=100)
    canvas.draw()

def daygraph():
    try:
        canvas.delete('all')
    except:
        pass
    a.plot(day('NDAQ')[0],day('^IXIC')[1],color='#E5CFAD')
    a.plot(day('^DJI')[0],day('^DJI')[1],color='#D392A4')
    a.plot(day('^GSPC')[0],day('^GSPC')[1],color='#98B7C3')
    a.set_facecolor('black')
    a.set_title ("Market", fontsize=16)
    a.set_ylabel("Price", fontsize=14)
    a.set_xlabel("5 minutes", fontsize=14)  
    canvas = FigureCanvasTkAgg(fig, master=market)
    canvas.get_tk_widget().place(x=100,y=100)
    canvas.draw()

Button(market, text='Past day',fg='black', bg='grey', relief=FLAT, command=lambda:daygraph()).place(x=0,y=300)
Button(market, text='Past 5 days',fg='black', bg='grey', relief=FLAT, command=lambda:weekgraph()).place(x=0,y=400) 
Button(market, text='Past year',fg='black', bg='grey', relief=FLAT, command=lambda:yeargraph()).place(x=0,y=500)    

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

root.mainloop()
#Launch Porgram
root.mainloop()
