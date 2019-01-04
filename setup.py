from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import requests
from rake_nltk import Rake
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmk"]
table2 = mydb["webSearch"]

r = Rake(min_length=2, max_length=2)

window = Tk()
window.configure(background='black')
window.title("Web Scraping")
window.geometry('800x500')

lbl = Label(window, text="Enter URL :",bg="black",fg="white")
url = Entry(window, width = 50)
lbl.grid( column = 10, row = 0 )
url.grid( column = 20, row = 1)
lbl.place(relx=0.5, rely=0.05, anchor=CENTER)
url.place(relx=0.5, rely=0.1, anchor=CENTER)

lbl2 = Label(window,text="Enter Keywords To Search :",bg="black",fg="white")
lbl2.grid( column = 10, row = 4 )
lbl2.place(relx=0.5, rely=0.3, anchor=CENTER)

url2 = Entry(window, width = 50)
url2.grid( column = 20, row = 5)
url2.place(relx=0.5, rely=0.35, anchor=CENTER)

lbl3 = Label(window,text="All Keywords :",bg="red",fg="white")
lbl3.grid( column = 10, row = 5 )
lbl3.place(relx=0.5, rely=0.52, anchor=CENTER)

T = Text(window, height=10, width=55)
T.pack()
T.place(relx=0.5, rely=0.75, anchor=CENTER)

def dataBase(data,fn1,fn2,fn3):
    row = {"url":data, "title":fn3, "text":fn1, "keywords":fn2}   
    table2.insert_one(row) 
    print("\n Success..")

def keyWord(dataLine):
    r.extract_keywords_from_text(dataLine)
    keyWords = """"""
    keyWords = r.get_ranked_phrases() 
    print(keyWords)
    return keyWords
    
def scrap(data):
    dataLine = """ """
    r = requests.get(data)
    Rdata = r.text
    soup = BeautifulSoup(Rdata, features="lxml")
    title = soup.find("title").string 
    for i in soup.find_all('p'):
        dataLine += i.text
    print(dataLine)
    return dataLine,title
        
def main():

    data = url.get()
    fn1,fn3 = scrap(data) #dataLine
    fn2 = keyWord(fn1)#keywords
    
    dataBase(data,fn1,fn2,fn3)    

    messagebox.showinfo('info','Success..!')

def display(ta,ua,tta,window2,txt):
   
    txt.insert(INSERT,"Title :\n" + ta + "\n\n")
    txt.insert(INSERT,"Url :\n" + ua + "\n\n")
    txt.insert(INSERT,"Text :\n" + tta + "\n\n\n")


def search():
    data2 = url2.get()
    myquery = { "keywords": data2 }
    mysearch = table2.find(myquery)

    window2 = Tk()
    window2.configure(background='black')
    window2.title("Web Scraping")
    window2.geometry('800x800')
    txt = scrolledtext.ScrolledText(window2,width=98,height=50) 
    txt.grid(column=0,row=0) 
    for u in table2.find(myquery): #loop for printing all result
        ta = u["title"]
        ua = u["url"]
        tta = u["text"]   
        display(ta,ua,tta,window2,txt)
  
    window.destroy()



 ### print available keywords
z = ""
for x in table2.find({},{ "_id": 0, "url": 0, "text": 0 ,"title":0}):
    y = x["keywords"]
    z += ", ".join(y)
T.insert(END, z)
###

btn = Button(window, text="Scrap", command=main,bg="green")
btn.grid(column=1, row=3)
btn.place(relx=0.5, rely=0.16, anchor=CENTER)

btn2 = Button(window, text="Search", command=search,bg="green")
btn2.grid(column=1, row=6)
btn2.place(relx=0.5, rely=0.41, anchor=CENTER)

window.mainloop()
