import sqlite3 as db
import csv

def create_tables():

    conn = db.connect("Orders.db")
    cur = conn.cursor()

    cur.execute("drop table if exists barcodes")

    cur.execute("drop table if exists orders")

    cur.execute("create table barcodes (barcode, order_id)")
    with open('barcodes.csv', 'r') as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [(i['barcode'], i['order_id']) for i in dr]

    cur.executemany("INSERT INTO barcodes (barcode, order_id) VALUES (?, ?);", to_db)

    cur.execute("create table orders (order_id, customer_id)")

    with open('orders.csv', 'r') as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [(i['order_id'], i['customer_id']) for i in dr]

    cur.executemany("INSERT INTO orders (order_id, customer_id) VALUES (?, ?);", to_db)

    conn.commit()
    conn.close()
    return db


def read_orders():
    ''''''


def read_barcodes():
    ''''''


def main():
    '''read orders'''
    '''read barcodes'''
    '''validate no order without bar code'''
    '''validate no dupicate bar codes'''
    '''join order to barcodes on order_id'''
    '''generate to output file'''
    '''group by customer amount of tickets, print top 5'''

if __name__ == "__main__":
    main()