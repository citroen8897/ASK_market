import mysql.connector
from mysql.connector import Error


def choisir_status_de_zakaz(new_zakaz_status, zakaz_id):
    try:
        conn = mysql.connector.connect(user='root',
                                       host='localhost',
                                       database='mysql')

        if conn.is_connected():
            new_status = f"UPDATE ASK_market_billing " \
                         f"SET status = '{new_zakaz_status}' " \
                         f"WHERE id = {zakaz_id}"
            cursor = conn.cursor()
            cursor.execute(new_status)
            print('Статус заказа успешно изменен!')
            conn.commit()
    except Error as error:
        print(error)
    finally:
        conn.close()
        cursor.close()
