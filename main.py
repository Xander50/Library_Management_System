import sqlite3 
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

connector= sqlite3.connect("library.db")
cursor=connector.cursor()

connector.execute("CREATE TABLE IF NOT EXISTS Library(BK_NAME TEXT, BK_ID TEXT PRIMARY KEY NOT NULL,AUTHOR_NAME TEXT, BK_STATUS TEXT,CARD_ID TEXT)")

root = Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0,0)

def issuer_card():
    cid=sd.askstring("Issuer Card ID","What is the Issuer's card ID\t\t\t")
    if not cid:
        mb.showerror("Issuer ID cannot be Zero!","Can't can't Issuer empty it must have a value")
    else:
        return cid
    
def display_records():
    global connector,cursor,tree
    tree.delete(*tree.get_children())
    cur=connector.execute('SELECT * from Library')
    data=cur.fetchall()
    for records in data:
        tree.insert('',END,values=records)

def clear_fields():
    global bk_status,bk_id,bk_name,author_name,card_id
    bk_status.set("Available")
    for i in ['bk_id','bk_name','author_name','card_id']:
        exec(f"{i}.set('')")
        bk_id_entry.config(state='normal')
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass


def clear_and_display():
    clear_fields()
    display_records()

def add_record():
    global connector
    global bk_name,bk_id,author_name,bk_status,card_id
    if(bk_status.get() == 'Issued'):
        card_id.set(issuer_card())
    else:
        card_id.set("N/A")
    surety=mb.askyesno("Are you sure?","Are you sure this is the data you want to enter?\n PLEASE NOTE THAT BOOK ID CANNOT BE CHANGED IN THE FUTURE")
    if(surety):
        try:
            connector.execute("INSERT INTO Library(BK_NAME,BK_ID,AUTHOR_NAME,BK_STATUS,CARD_ID) VALUES(?,?,?,?,?)",(bk_name.get(),bk_id.get(),author_name.get(),bk_status.get(),card_id.get()))
            connector.commit()
            clear_and_display()
            mb.showinfo("records added","The New record was sucessfully added to your database")
        except sqlite3.IntegrityError:
            mb.showerror("Book ID already in use","Book ID you are trying to enter is already in the data base, please alter that book record or check any discrepancy")

def view_record():
    global bk_name,bk_id,bk_status,author_name,card_id
    global tree
    if not tree.focus():
        mb.showerror("select a row!","To view a record you must select it on the table")
        return
    curret_item_selected=tree.focus()
    values_in_selected_item=tree.item(curret_item_selected)
    selection=values_in_selected_item['values']
    bk_name.set(selection[0]);bk_id.set(selection[1]);author_name.set(selection[2]);bk_status.set(selection[3])
    try:
        card_id.set(selection[4])
    except:
        card_id.set('')


def update_record():
    def update():
        global bk_status,bk_id,bk_name,author_name,card_id
        global connector,tree
        if bk_status.get()=="Issued":
            card_id.set(issuer_card())
        else:
            card_id.set('N/A')
        cursor.execute("UPDATE Library SET BK_NAME=?,AUTHOR_NAME=?,BK_STATUS=?,CARD_ID=? WHERE BK_ID=?",(bk_name.get(),bk_id.get(),author_name.get(),bk_status.get(),card_id.get()))
        connector.commit()
        clear_and_display()
        edit.destroy()
        bk_id_entry.config(state="normal")
        clear.config(state='normal')
    view_record()
    bk_id_entry.config(state='disable')
    clear.config(state='disable')
    edit=Button(left_frame,text="Update record",font=button_font,bg=btn_bg,width=20,command=update)
    edit.place(x=40,y=370)

def remove_record():
    if not tree.selection():
        mb.showerror("Error","Please select an item from the data base")
        return
    current_item = tree.focus()
    values=tree.item(current_item) 
    selection=values["values"]
    cursor.execute("delete from library where bk_id=?",(selection[1],))
    connector.commit()
    tree.delete(current_item)
    mb.showinfo("Done","Record was deleted")
    clear_and_display()
    

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

Label(root,text='Library Management System', font=('Noto Sans CJK TC',16,'bold'),fg='black').pack(side=TOP,fill=X)
left_frame = Frame(root,bg=left_bg)
left_frame.place(x=0,y=30,relwidth=0.3,relheight=0.9)

right_frame=Frame(root,bg=right_bg)
right_frame.place(relx=0.3,y=32,relheight=0.3,relwidth=0.7)

rb_frame=Frame(root)
rb_frame.place(relx=.3,rely=.2,relheight=.7,relwidth=.7)

Label(left_frame,text='Book Name',bg=left_bg,font=lbl_font).place(x=98,y=25)
Entry(left_frame,width=25,font=entry_font,text=bk_name).place(x=45,y=55)

Label(left_frame,text='Book ID',bg=left_bg,font=lbl_font).place(x=110,y=80)
bk_id_entry=Entry(left_frame,width=25,font=entry_font,text=bk_id).place(x=45,y=105)

Label(left_frame,text='Author Name',bg=left_bg,font=lbl_font).place(x=90,y=135)
Entry(left_frame,width=25,font=entry_font,text=author_name).place(x=45,y=160)

Label(left_frame,text='Book Status',bg=left_bg,font=lbl_font).place(x=90,y=190)
menu=OptionMenu(left_frame,bk_status,*['Available','Issued'])
menu.configure(font=entry_font,width=12)
menu.place(x=75,y=215)

update=Button(left_frame,text="Update Record",font=button_font,bg=btn_bg,width=20,command=add_record)
update.place(x=50,y=325)

clear=Button(left_frame,text="Clear Fields",font=button_font,bg=btn_bg,width=20,command=clear_fields)
clear.place(x=50,y=395)

Button(right_frame,text="Delete Book Record",font=button_font,bg=btn_bg,width=17,command=remove_record).place(x=8,y=20)

Button(right_frame,text="Delete Full Inventory",font=button_font,bg=btn_bg,width=17).place(x=178,y=20)

Button(right_frame,text="Update Book Details",font=button_font,bg=btn_bg,width=17,command=update_record).place(x=348,y=20)

Button(right_frame,text="Change Book availability",font=button_font,bg=btn_bg,width=19).place(x=518,y=20)

Label(rb_frame,text="BOOK INVENTORY",bg="lightgreen",font=("Noto Sans CJK TC", 15, "bold")).pack(side=TOP,fill=X)

tree=ttk.Treeview(rb_frame,selectmode=BROWSE,columns=("Book name","BookID", "Author","Book status","Issuer Card ID"))
tree.heading("Book name",text="Book name",anchor=CENTER)
tree.heading("BookID",text="Book ID",anchor=CENTER)
tree.heading("Author",text="Author",anchor=CENTER)
tree.heading("Book status",text="Book status",anchor=CENTER)
tree.heading("Issuer Card ID",text="Issuer Card ID",anchor=CENTER)

tree.column("#0",width=0,stretch=NO)
tree.column("#1",width=225,stretch=NO)
tree.column("#2",width=70,stretch=NO)
tree.column("#3",width=150,stretch=NO)
tree.column("#4",width=105,stretch=NO)
tree.column("#5",width=134,stretch=NO)
tree.place(y=30,x=0,relheight=0.9,relwidth=1)

xScrollBar = Scrollbar(tree,orient=HORIZONTAL)
yScrollBar = Scrollbar(tree,orient=VERTICAL)
xScrollBar.pack(side=BOTTOM)
yScrollBar.pack(side=RIGHT)
tree.config(xscrollcommand=xScrollBar.set,yscrollcommand=yScrollBar.set)

clear_and_display()
root.update()
root.mainloop()