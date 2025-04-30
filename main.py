import mysql.connector as mc
from tkinter import *


def win2():
    win2 = Tk()
    win2.title("Редактирование партнеров")
    Label(win2,text="Название").grid(row=0, column=0)
    Label(win2, text="Тип").grid(row=1, column=0)
    Label(win2, text="Страна").grid(row=2, column=0)
    Label(win2, text="Год основания").grid(row=3, column=0)

    win.withdraw() #скрыть первое окно
    win2.mainloop()


def skidka(_summa):
    if _summa < 500:
        return 0
    else:
        return 10


win = Tk()
win.title("Информация о партнерах")
partners = []
partners_var = Variable(value=partners)
partners_view = Listbox(width=70,
                        listvariable=partners_var)
to_win_2 = Button(text="Редактирование", command=win2)
partners_view.grid(row=0, column=0)
to_win_2.grid(row=1, column=0)

cnx = mc.connect(host="localhost",
                 user="pk31",
                 password="1234",
                 database="partners")
cur = cnx.cursor()
sql = """SELECT partners.Name, partners.Country,
                partners.Founded, SUM(sales.quantity)
        FROM partners
        JOIN sales
        ON partners.ID = sales.id_partner
        GROUP BY partners.Name
        LIMIT 10"""
cur.execute(sql)
ans = cur.fetchall()
for item in ans:
    partners.append(f"Название:{item[0]}, Скидка:{skidka(item[3])}")
partners_var.set(partners)
win.mainloop()
