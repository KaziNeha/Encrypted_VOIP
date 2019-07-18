from Tkinter import *
import Tkinter
from PIL import Image, ImageTk

Voip_Frame_key_page = Tk()

Voip_Frame_key_page.title("Encryptsy")
Voip_Frame_key_page.geometry('500x600')
Voip_Frame_key_page.configure(background = 'white')

logo=ImageTk.PhotoImage(Image.open("logo1.png"))
logoLbl = Label(Voip_Frame_key_page, borderwidth= 0, highlightthickness = 0, image=logo).place(x=215, y=30)

logo_text=ImageTk.PhotoImage(Image.open("logo_text.png"))
logot = Label(Voip_Frame_key_page, borderwidth= 0, highlightthickness = 0, image=logo_text).place(x=150, y=105)
call = Label(Voip_Frame_key_page, text="Enter SecID",font='Helvetica 18 bold',foreground='gray',background='white').place(x=190, y=200)
ip1= Entry(Voip_Frame_key_page,  width = 40)
ip1.place(x=145, y= 230)

#head = Label(Voip_Frame_key_page, text= "Attach key & click on textbox", font='Helvetica 18 bold', foreground= 'gray' , background = 'white').place(x=80, y= 230)

#ip2= Entry(Voip_Frame_key_page,  width = 60)
#ip2.place(x=60, y= 270)


#keybutton=PhotoImage(file="key_button.gif")
#a=Button(Voip_Frame_key_page,image=keybutton,bg='white')
#a.place(x=210,y=320)

#Voip_Frame_key_page['bg']='white'
callbutton=PhotoImage(file="green_button.gif")
b=Button(Voip_Frame_key_page,image=callbutton,bg='white')
b.place(x=100,y=460)

#Voip_Frame_key_page['bg']='white'
endbutton=PhotoImage(file="red_button.gif")
b=Button(Voip_Frame_key_page,image=endbutton,bg='white')
b.place(x=300,y=460)


Voip_Frame_key_page.mainloop()
