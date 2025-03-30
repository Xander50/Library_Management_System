from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

root = Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0,0)

left_bg='lime'
right_bg='green'
btn_bg='yellow'

lbl_font=("Georgia",13)
entry_font=("Times New Roman",12)
button_font=("Gill Sans MT",13)

bk_status=StringVar()
bk_name = StringVar()
bk_id=StringVar()
author_name=StringVar()
card_id=StringVar()

Label(root,text='Library Management System', font=('Noto Sans CJK TC',16,'bold'),fg='black').pack(side=TOP)
left_frame = Frame(root,bg=left_bg)
left_frame.place(x=0,y=30,relwidth=0.3,relheight=0.9)

right_frame=Frame(root,bg=right_bg)
right_frame.place(relx=0.3,y=32,relheight=0.3,relwidth=0.7)

rb_frame=Frame(root)
rb_frame.place(relx=.3,rely=.2,relheight=.7,relwidth=.7)

Label(left_frame,text='Book Name',bg=left_bg,font=lbl_font).place(x=98,y=25)
Entry(left_frame,width=25,font=entry_font,text=bk_name).place(x=45,y=55)

Label(left_frame,text='Book ID',bg=left_bg,font=lbl_font).place(x=110,y=80)
Entry(left_frame,width=25,font=entry_font,text=bk_id).place(x=45,y=105)

Label(left_frame,text='Author Name',bg=left_bg,font=lbl_font).place(x=90,y=135)
Entry(left_frame,width=25,font=entry_font,text=author_name).place(x=45,y=160)

Label(left_frame,text='Book Status',bg=left_bg,font=lbl_font).place(x=90,y=190)
menu=OptionMenu(left_frame,bk_status,*['Available','Issued'])
menu.configure(font=entry_font,width=12)
menu.place(x=75,y=215)

update=Button(left_frame,text="Update Record",font=button_font,bg=btn_bg,width=20)
update.place(x=50,y=325)

delete_fields=Button(left_frame,text="Clear Fields",font=button_font,bg=btn_bg,width=20)
delete_fields.place(x=50,y=395)

root.mainloop()