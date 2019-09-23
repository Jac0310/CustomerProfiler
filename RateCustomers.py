import sqlite3 as db
import csv
import sys


def create_tables():

    conn = db.connect("Orders.db")
    cur = conn.cursor()

    cur.execute("drop table if exists barcodes")

    cur.execute("drop table if exists orders")

    cur.execute("create table barcodes (barcode, order_id)")

    with open('barcodes.csv', 'r') as fin:
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

'''Refactor into database class'''
def executeQuery(query):
    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall(), conn

def executeNonQuery(query):
    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()

def validate_barcodes():
    # validate no duplicate bar codes

    dic, conn = executeQuery("Select count(barcode), barcode from barcodes group by barcode having count(barcode) > 1")

    if dic is not None:
        print("Deleting duplicate barcodes found for: " + ", ".join(str(v) for k, v in dic), file=sys.stderr)

        executeNonQuery("delete from barcodes where barcode in"
                        "(select barcode from(Select count(barcode),barcode from barcodes "
                        "group by barcode having count(barcode) > 1))")

def validate_orders():
    # validate no order without bar code

    res, conn = executeQuery("select order_id from orders o where not exists "
                "(select 1 from barcodes b where b.order_id = o.order_id )")
    conn.close()
    if res is not None:
        print("Deleting orders with no barcode: " + ", ".join(str(i[0]) for i in res), file=sys.stderr)

        executeNonQuery("delete from orders where order_id in("
                    "select order_id from orders o where not exists "
                    "(select 1 from barcodes b where b.order_id = o.order_id ))")

def get_customer_to_order():
    data, conn = executeQuery("select o.customer_id, o.order_id, group_concat(b.barcode, ', ') from orders o, barcodes b "
                "where b.order_id = o.order_id "
                "group by o.customer_id, o.order_id")
    conn.close()
    return data

def write_to_csv(data):
    with open('customers.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['customer_id', 'order_id', 'barcodes'])
        writer.writerows(data)
        f.close()

def get_top_five():
    res, conn = executeQuery("select o.customer_id, count(b.barcode) from orders o, barcodes b "
                 "where b.order_id = o.order_id "
                 "group by o.customer_id "
                 "order by count(b.barcode) desc")
    conn.close()
    return (str(res[i][0]) for i in range(0, 5))

def get_unused_barcodes():
    res, conn = executeQuery("select count(barcode) from barcodes where order_id = ''")
    conn.close()
    return res[0][0]


def main():
    create_tables()
    validate_barcodes()
    validate_orders()
    dataset = get_customer_to_order()
    write_to_csv(dataset)
    print("The top 5 customers are: " + ", ".join(get_top_five()))
    print("There are: " + str(get_unused_barcodes()) + " unused barcodes.")



if __name__ == "__main__":
    main()