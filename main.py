import tkinter.messagebox as mb
import mysql.connector as mc
from tkinter import *


def create_db_connection():
    """Создает и возвращает соединение с базой данных"""
    try:
        return mc.connect(
            host="localhost",
            user="pk31",
            password="1234",
            database="partners"
        )
    except mc.Error as err:
        mb.showerror("Ошибка", f"Ошибка подключения к БД: {err}")
        return None


def close_db_resources(cursor=None, connection=None):
    """Закрывает ресурсы БД"""
    if cursor:
        cursor.close()
    if connection:
        connection.close()


def add_partner():
    """Добавляет нового партнера в базу данных"""
    fields = [
        name_entry.get(),
        type_entry.get(),
        country_entry.get(),
        year_entry.get()
    ]

    if not all(fields):
        mb.showwarning("Предупреждение", "Все поля должны быть заполнены")
        return

    cnx = create_db_connection()
    if not cnx:
        return

    try:
        with cnx.cursor() as cur:
            sql = """INSERT INTO partners(Name, Country, type, Founded)
                     VALUES(%s, %s, %s, %s)"""
            cur.execute(sql, fields)
            cnx.commit()
            mb.showinfo("Успех", "Партнер успешно добавлен")
            refresh_partners_list()
    except mc.Error as err:
        mb.showerror("Ошибка", f"Ошибка при добавлении: {err}")
    finally:
        close_db_resources(connection=cnx)


def refresh_partners_list():
    """Обновляет список партнеров в интерфейсе"""
    cnx = create_db_connection()
    if not cnx:
        return

    try:
        with cnx.cursor() as cur:
            cur.execute("SELECT * FROM partners")
            partners = [
                f"Название:{item[1]}, страна:{item[2]}, тип:{item[3]}, год:{item[4]}"
                for item in cur.fetchall()
            ]
            part_list_var.set(partners)
    except mc.Error as err:
        mb.showerror("Ошибка", f"Ошибка загрузки данных: {err}")
    finally:
        close_db_resources(connection=cnx)


def calculate_discount(total):
    """Рассчитывает скидку на основе суммы"""
    if total < 500:
        return 0
    elif 500 <= total < 1000:
        return 10
    elif 1000 <= total < 2000:
        return 15
    return 20


def create_partners_window():
    """Создает главное окно с информацией о партнерах"""
    win = Tk()
    win.title("Информация о партнерах")

    # Список партнеров
    partners_list = Listbox(win, width=70)
    partners_list.grid(row=0, column=0, padx=10, pady=10)

    # Кнопка редактирования
    Button(
        win,
        text="Редактирование",
        command=create_edit_window
    ).grid(row=1, column=0, pady=5)

    # Загрузка данных
    cnx = create_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cur:
                cur.execute("""
                    SELECT partners.Name, SUM(sales.quantity)
                    FROM partners
                    JOIN sales ON partners.ID = sales.id_partner
                    GROUP BY partners.Name
                    LIMIT 10
                """)
                for name, quantity in cur.fetchall():
                    partners_list.insert(
                        END,
                        f"Название: {name}, Скидка: {calculate_discount(quantity)}%"
                    )
        except mc.Error as err:
            mb.showerror("Ошибка", f"Ошибка загрузки данных: {err}")
        finally:
            close_db_resources(connection=cnx)

    return win


def create_edit_window():
    """Создает окно редактирования партнеров"""
    win = Toplevel()
    win.geometry("450x450")
    win.title("Редактирование партнеров")

    # Поля ввода
    fields = [
        ("Название", 0),
        ("Тип", 1),
        ("Страна", 2),
        ("Год основания", 3)
    ]

    entries = []
    for text, row in fields:
        Label(win, text=text).grid(row=row, column=0, sticky=W, padx=5, pady=5)
        entry = Entry(win)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries.append(entry)

    global name_entry, type_entry, country_entry, year_entry, selected_partner, part_view
    name_entry, type_entry, country_entry, year_entry = entries

    # Список партнеров
    global part_list_var
    part_list_var = StringVar()
    part_view = Listbox(
        win,
        listvariable=part_list_var,
        width=50,
        height=12
    )
    part_view.grid(row=4, column=0, columnspan=2, pady=10)

    # Кнопки
    Button(
        win,
        text="Добавить",
        command=add_partner
    ).grid(row=5, column=0, padx=5, pady=5, sticky=EW)

    Button(
        win,
        text="Редактировать",
        command=edit_partner
    ).grid(row=5, column=1, padx=5, pady=5, sticky=EW)

    refresh_partners_list()


def edit_partner():
    """Редактирует выбранного партнера"""
    selected = part_view.curselection()
    if not selected:
        mb.showwarning("Предупреждение", "Выберите партнера для редактирования")
        return

    fields = [
        name_entry.get(),
        type_entry.get(),
        country_entry.get(),
        year_entry.get()
    ]

    if not all(fields):
        mb.showwarning("Предупреждение", "Все поля должны быть заполнены")
        return

    cnx = create_db_connection()
    if not cnx:
        return

    try:
        with cnx.cursor() as cur:
            # Получаем ID выбранного партнера
            cur.execute("SELECT ID FROM partners LIMIT 1 OFFSET %s", (selected[0],))
            partner_id = cur.fetchone()[0]

            sql = """UPDATE partners 
                         SET Name = %s, Country = %s, type = %s, Founded = %s
                         WHERE ID = %s"""
            cur.execute(sql, (*fields, partner_id))
            cnx.commit()
            mb.showinfo("Успех", "Данные партнера успешно обновлены")
            refresh_partners_list()
    except mc.Error as err:
        mb.showerror("Ошибка", f"Ошибка при редактировании: {err}")
    finally:
        close_db_resources(connection=cnx)


if __name__ == "__main__":
    app = create_partners_window()
    app.mainloop()
