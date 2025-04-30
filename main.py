import tkinter.messagebox

import mysql.connector as mc
from tkinter import *


def add_partner():
    name = name_entry.get()
    type = type_entry.get()
    country = country_entry.get()
    year = year_entry.get()
    if name and type and country and year:
        cnx = mc.connect(host="localhost",
                         user="pk31",
                         password="1234",
                         database="partners")
        cur = cnx.cursor()
        sql = """INSERT INTO partners(Name,Country,type,Founded)
                VALUES(%s,%s,%s,%s)"""
        params = (name, country, type, year)
        cur.execute(sql, params)
        cnx.commit()
        tkinter.messagebox.showinfo("Запрос",
                                    "Выполнен успешно")


def win21():
    global name_entry
    global type_entry
    global country_entry
    global year_entry
    global part_list_var
    global part_view

    win2 = Toplevel()  # Изменено с Tk() на Toplevel() для правильной работы с несколькими окнами
    win2.geometry("400x400")  # Увеличено для лучшего отображения
    win2.title("Редактирование партнеров")

    # Поля ввода
    Label(win2, text="Название").grid(row=0, column=0)
    name_entry = Entry(win2)
    name_entry.grid(row=0, column=1)

    Label(win2, text="Тип").grid(row=1, column=0)
    type_entry = Entry(win2)
    type_entry.grid(row=1, column=1)

    Label(win2, text="Страна").grid(row=2, column=0)
    country_entry = Entry(win2)
    country_entry.grid(row=2, column=1)

    Label(win2, text="Год основания").grid(row=3, column=0)
    year_entry = Entry(win2)
    year_entry.grid(row=3, column=1)

    # Список партнеров
    part_list = []
    part_list_var = Variable(value=part_list)
    part_view = Listbox(win2, listvariable=part_list_var, width=40, height=10)
    part_view.grid(row=4, column=0, columnspan=2, pady=10)

    # Кнопки
    add_btn = Button(win2, text="Добавить", command=add_partner)
    add_btn.grid(row=5, column=0, padx=5, pady=5)

    edit_btn = Button(win2, text="Редактировать")
    edit_btn.grid(row=5, column=1, padx=5, pady=5)

    # Загрузка данных из БД
    try:
        cnx = mc.connect(host="localhost",
                         user="pk31",
                         password="1234",
                         database="partners")
        cur = cnx.cursor()
        cur.execute("SELECT * FROM partners")
        ans = cur.fetchall()

        part_list.clear()  # Очищаем список перед заполнением
        for item in ans:
            tmp = f"Название:{item[1]}, страна:{item[2]}, тип:{item[3]}, год:{item[4]}"
            part_list.append(tmp)

        part_list_var.set(part_list)
    except mc.Error as err:
        tkinter.messagebox.showerror("Ошибка", f"Ошибка БД: {err}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'cnx' in locals(): cnx.close()


def skidka(_summa):
    if _summa < 500:
        return 0
    elif 500 < _summa < 1000:
        return 10
    elif 1000 < _summa < 2000:
        return 15
    else:
        return 20


win = Tk()
win.title("Информация о партнерах")
partners = []
partners_var = Variable(value=partners)
partners_view = Listbox(width=70,
                        listvariable=partners_var)
to_win_2 = Button(text="Редактирование", command=win21)
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
