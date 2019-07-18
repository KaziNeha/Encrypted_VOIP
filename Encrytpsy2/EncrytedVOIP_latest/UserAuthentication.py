import sqlite3
from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import os
import threading
from GUI import GUI

user = None
paswd = None
msg = None
class userDatabase():
    def __init__(self):
        try:
            self.conn = sqlite3.connect('GoSecure.db')
            print("Database connected")
        except  Exception as e:
            print (e)
        try:
            self.conn.execute("""CREATE TABLE Credentials  
            ( Sr_no INTEGER PRIMARY KEY AUTOINCREMENT ,
            ID INT UNIQUE ,
            Password VARCHAR(20))
            """)
            print ("Created table for Credentials")
        except Exception as e:
            print(e)


    def insertUser(self, id, paswd):
        try:
            self.conn.execute("INSERT INTO Credentials(ID, Password) VALUES (?,? )", (id, paswd))
            self.conn.commit()
            print ("RECORDS INSERTED")
        except Exception as e:
            print(e)


    def getData(self):
        global user, paswd, msg
        print(user.get())
        try:
            res = self.conn.execute('''SELECT * FROM Credentials WHERE ID = ? AND Password = ? ''', (int(user.get()), str(paswd.get())))
            if(len(res.fetchall())):
                print("Acess Granted")
                Voip_Frame.destroy()
                GUI()
            else:
                print("Access Denied")
                msg.set("Invalid Credentials")
                print(msg.get())
        except Exception as e:
            print(e)

    def Closeconn(self):
        self.conn.close()






if __name__ == '__main__':

    users = userDatabase()
    users.insertUser(9819, '1233456678')

    global user, paswd, msg

    Voip_Frame = Tk()
    msg = Tkinter.StringVar()
    paswd = Tkinter.StringVar()
    user = Tkinter.StringVar()

    Voip_Frame.title("GoSecure")
    Voip_Frame.geometry('900x500')
    Voip_Frame.configure(background='gray15')
    head = Label(Voip_Frame, text="ENCRYPTSY", font='Helvetica 18 bold', foreground='white',
                 background='gray15').place(x=350, y=10)
    logo = ImageTk.PhotoImage(Image.open("wall.JPG"))
    logoLbl = Label(Voip_Frame, borderwidth=0, highlightthickness=0, image=logo).place(x=320, y=65)



    Label(Voip_Frame, text = "User ID:", width = 10, font='Helvetica 9 bold').place(x = 250,y = 270)
    userName = Entry(Voip_Frame, width=40, textvariable=user)
    userName.place(x=350, y=270)



    Label(Voip_Frame, text = "Password:", width = 10, font='Helvetica 9 bold').place(x = 250,y = 320)
    password = Entry(Voip_Frame, width=40, textvariable=paswd, show = "*")
    password.place(x=350, y=320)


    login = Button(Voip_Frame, width=10, text="Login", font='bold', command =users.getData)
    login.config(background='green')
    login.place(x=360, y=380)


    call = Label(Voip_Frame, textvariable=msg, font='Helvetica 12 bold', foreground='red',
                 background='gray15').place(x=320, y=440)


    Voip_Frame.mainloop()

