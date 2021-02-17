import product
import mysql.connector
from mysql.connector import Error


def get_products_db():
    products_data_base = []
    try:
        conn = mysql.connector.connect(user='root',
                                       host='localhost',
                                       database='mysql')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ASK_market_products")
            row = cursor.fetchone()
            while row is not None:
                products_data_base.append(product.Product(row[0], row[1],
                                                          row[2], row[3],
                                                          row[4], row[5]))
                row = cursor.fetchone()
            conn.commit()
    except Error as error:
        print(error)
    finally:
        conn.close()
        cursor.close()
    return products_data_base
