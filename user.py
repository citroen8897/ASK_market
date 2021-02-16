import re
import mysql.connector
from mysql.connector import Error
import password_generator


class User:
    def __init__(self, user_id, email, telephone, password, nom, prenom,
                 status):

        self.user_id = user_id

        self.email = email
        while not re.search(r"\w+\.*\w+@\w+\.\w+", self.email):
            self.email = input('Введите электронный адрес: ')

        self.telephone = telephone
        while True:
            for element in self.telephone:
                if not element.isdigit():
                    self.telephone = self.telephone.replace(element, "")
            if len(self.telephone) < 10:
                self.telephone = input('Введите телефон: ')
            else:
                if not self.telephone.startswith("+38"):
                    self.telephone = "+38" + self.telephone[-10:]
                    break

        self.password = password
        while len(self.password) < 6:
            print('Пароль должен содержать минимум 6 символов')
            self.password = input('Введите пароль: ')

        self.nom = nom
        while not self.nom.isalpha():
            self.nom = (input('Введите имя: ')).title()

        self.prenom = prenom
        while not self.prenom.isalpha():
            self.prenom = (input('Введите фамилию: ')).title()

        self.status = status
        self.basket = []

    def __str__(self):
        return f'user id: {self.user_id}\n' \
               f'e-mail: {self.email}\n' \
               f'телефон: {self.telephone}\n' \
               f'пароль: {self.password}\n' \
               f'имя: {self.nom}\n' \
               f'фамилия: {self.prenom}\n' \
               f'статус: {self.status}\n'

    def add_user_data_base(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_user = "INSERT INTO ASK_market_users" \
                           "(email,telephone,password,nom,prenom," \
                           "status) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                self.password = \
                    password_generator.generator_de_password(self.password)
                cursor.execute(new_user, (self.email, self.telephone,
                                          self.password, self.nom,
                                          self.prenom, self.status))
                if cursor.lastrowid:
                    print('успешно добавлена запись. id пользователя: ',
                          cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_basket(self):
        if len(self.basket) == 0:
            print('Корзина пуста...')
        else:
            print('\nВаша корзина:')
            j = 1
            total_prix = 0
            for element in self.basket:
                print(f'{j}. {element.nom} {element.prix}')
                j += 1
                total_prix += element.prix
            print(f'\nОбщая сумма товаров в корзине: {total_prix}')

    def make_zakaz(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_zakaz = "INSERT INTO ASK_market_billing" \
                            "(summa, status, id_user) VALUES(%s,%s,%s)"
                cursor = conn.cursor()
                total_prix = 0
                for element in self.basket:
                    total_prix += element.prix
                cursor.execute(new_zakaz, (total_prix, 'в обработке',
                                           self.user_id))
                if cursor.lastrowid:
                    print('Заказ успешно оформлен.\nНомер заказа: ',
                          cursor.lastrowid)
                    numero_de_zakaz = cursor.lastrowid
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
        return numero_de_zakaz

    def make_zakaz_full(self, numero_de_zakaz, product_id, product_nom,
                        user_id, user_email):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_zakaz = "INSERT INTO ASK_market_full_orders" \
                            "(numero_de_zakaz, product_id, product_nom, " \
                            "user_id, user_email) VALUES(%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                cursor.execute(new_zakaz, (numero_de_zakaz, product_id,
                                           product_nom, user_id, user_email))
                if cursor.lastrowid:
                    print('Успешно добавлена запись...', cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_history_des_zakazes(self):
        zakazes_data_base = []
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')
            if conn.is_connected():
                cursor = conn.cursor()
                if self.status == 'user':
                    cursor.execute(f"SELECT * FROM ASK_market_billing WHERE "
                                   f"id_user={self.user_id}")
                elif self.status == 'admin':
                    cursor.execute(f"SELECT * FROM ASK_market_billing ")
                row = cursor.fetchone()
                while row is not None:
                    zakazes_data_base.append({'№ заказа: ': row[0],
                                              'сумма: ': row[1],
                                              'дата/время: ': row[2],
                                              'статус заказа: ': row[3]})
                    row = cursor.fetchone()
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
        return zakazes_data_base

    def get_full_info_de_zakaz(self, numero_de_zakaz):
        info_de_zakaz = []
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM ASK_market_full_orders "
                               f"WHERE numero_de_zakaz={numero_de_zakaz}")
                row = cursor.fetchone()
                while row is not None:
                    info_de_zakaz.append({'id товара': row[2],
                                          'название товара': row[3],
                                          'id клиента: ': row[4]})
                    row = cursor.fetchone()
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
        return info_de_zakaz
