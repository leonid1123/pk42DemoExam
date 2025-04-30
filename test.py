import tkinter

win=tkinter.Tk()
lst=["1","2"]
lst_var = tkinter.Variable(value=lst)
view = tkinter.Listbox(listvariable=lst_var)
view.pack()
lst.append("3")
lst_var.set(lst)

l2=["4","5"]
lv2 = tkinter.Variable(value=l2)
v2 = tkinter.Listbox(listvariable=lv2)
v2.pack()
win.mainloop()