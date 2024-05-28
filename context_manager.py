import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_params = {
    'database': os.getenv('database'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
}


try:
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            select_all_products = """select * from product;"""
            cursor.execute(select_all_products)
            for i in cursor.fetchall():
                print(i)

except psycopg2.errors.UndefinedTable as error:
    conn.rollback()
    print(error)


class ConnectDB:
    def __init__(self, db_params: dict):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        self.cur = self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        if self.conn:
            self.cur.close()
            self.conn.close()

    def commit(self):
        self.conn.commit()


class Product:
    def __init__(self, name):
        self.name = name

    def save(self):
        with ConnectDB(db_params) as db:
            insert_into_product = """INSERT INTO n47.public.product(name)
            values (%s);
            """
            db.cur.execute(insert_into_product, (self.name,))
            db.commit()
            print('Successfully saved')


product = Product('chanyutgich')
product.save()
