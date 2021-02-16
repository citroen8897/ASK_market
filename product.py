import re
import mysql.connector
from mysql.connector import Error


class Product:
    def __init__(self, product_id, nom, etre, q_1, q_2, prix):
        self.product_id = product_id

        self.nom = nom
        while not re.findall(r'[a-zA-Zа-яА-Я0-9]', self.nom):
            self.nom = input('Введите название товара: ')

        self.etre = etre
        self.q_list = ['1', 'в наличии', '2', 'нет в наличии', '3',
                       'ожидается', '4', 'под заказ', '5',
                       'снято с производства']
        while self.etre not in self.q_list:
            print('Необходимо задать статус наличия товара\n'
                  'Выберите статус согласно цифровому идентификатору\n'
                  'Возможные статусы:\n'
                  '1 - в наличии\n'
                  '2 - нет в наличии\n'
                  '3 - ожидается\n'
                  '4 - под заказ\n'
                  '5 - снято с производства\n')
            self.etre = input('Введите статус наличия товара: ')

        self.q_1 = str(q_1)
        while re.findall(r'[^0-9.]', self.q_1) or len(self.q_1) == 0:
            self.q_1 = input('Введите количество в единице товара: ')
        self.q_1 = float(self.q_1)

        self.q_2 = q_2
        while re.findall(r'[^a-zA-Zа-яА-Я.]', self.q_2) or len(self.q_2) == 0:
            self.q_2 = input('Введите единицу измерения товара: ')

        self.prix = str(prix)
        while re.findall(r'[^0-9.]', self.prix) or len(self.prix) == 0:
            self.prix = input('Введите цену за единицу товара: ')
        self.prix = float(self.prix)

    def __str__(self):
        return f'id товара: {self.product_id}\n' \
               f'название: {self.nom}\n' \
               f'наличие: {self.etre}\n' \
               f'в единице товара: {self.q_1} {self.q_2}\n' \
               f'цена за ед.: {self.prix}\n'

    def add_product_data_base(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_user = "INSERT INTO ASK_market_products" \
                           "(nom,etre,q_1,q_2,prix) VALUES(%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                self.etre = self.q_list[self.q_list.index(self.etre) + 1]
                cursor.execute(new_user, (self.nom, self.etre, self.q_1,
                                          self.q_2, self.prix))
                if cursor.lastrowid:
                    print('успешно добавлена запись. id товара: ',
                          cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_status(self, new_product_status):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                self.etre = new_product_status
                self.etre = self.q_list[self.q_list.index(self.etre) + 1]
                new_status = f"UPDATE ASK_market_products " \
                             f"SET etre = '{self.etre}' " \
                             f"WHERE id = {self.product_id}"
                cursor = conn.cursor()
                cursor.execute(new_status)
                print('Статус товара успешно изменен!')
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_prix(self, new_product_prix):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                self.prix = new_product_prix
                new_prix = f"UPDATE ASK_market_products " \
                           f"SET prix = '{self.prix}' " \
                           f"WHERE id = {self.product_id}"
                cursor = conn.cursor()
                cursor.execute(new_prix)
                print('Цена товара успешно изменена!')
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_nom(self, new_product_nom):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                self.nom = new_product_nom
                new_nom = f"UPDATE ASK_market_products " \
                           f"SET nom = '{self.nom}' " \
                           f"WHERE id = {self.product_id}"
                cursor = conn.cursor()
                cursor.execute(new_nom)
                print('Название товара успешно изменено!')
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
