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
            res = self.conn.execute('''SELECT * FROM Credentials WHERE ID = ? AND Password = ? ''',
                                    (int(user.get()), str(paswd.get())))
            if (len(res.fetchall())):
                print("Acess Granted")
                Voip_Frame_login_page.destroy()
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

    Voip_Frame_login_page = Tk()
    user = Tkinter.StringVar()
    paswd = Tkinter.StringVar()

    Voip_Frame_login_page.title("Encryptsy")
    Voip_Frame_login_page.geometry('500x600')
    Voip_Frame_login_page.configure(background='white')

    logo = ImageTk.PhotoImage(Image.open("logo1.png"))
    logoLbl = Label(Voip_Frame_login_page, borderwidth=0, highlightthickness=0, image=logo).place(x=215, y=50)

    logo_text = ImageTk.PhotoImage(Image.open("logo_text.png"))
    logot = Label(Voip_Frame_login_page, borderwidth=0, highlightthickness=0, image=logo_text).place(x=150, y=125)

    user_logo = ImageTk.PhotoImage(Image.open("fusername.png"))
    logou = Label(Voip_Frame_login_page, borderwidth=0, highlightthickness=0, image=user_logo).place(x=50, y=200)

    ip1 = Entry(Voip_Frame_login_page, width=60, textvariable=user)
    ip1.place(x=90, y=200)

    pwd_logo = ImageTk.PhotoImage(Image.open("fpassword.png"))
    logop = Label(Voip_Frame_login_page, borderwidth=0, highlightthickness=0, image=pwd_logo).place(x=50, y=250)

    ip = Entry(Voip_Frame_login_page, width=60, show='*', textvariable=paswd)
    ip.place(x=90, y=250)

    sign_in = Button(Voip_Frame_login_page, width=10, text="SIGN IN", font='bold', fg='white',
                     command=users.getData)  # , command=MakeCall)
    sign_in.config(background='gray15')
    sign_in.place(x=205, y=290)

    Voip_Frame_login_page.mainloop()
