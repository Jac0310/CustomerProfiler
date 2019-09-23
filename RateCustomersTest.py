from RateCustomers import *
import pytest


def test_create_tables():
    db = create_tables()
    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute("select * from barcodes")
    print(cur.fetchall())
    conn.close()

    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute("select * from orders")
    print(cur.fetchall())
    conn.close()

    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute("drop table barcodes")
    cur.execute("drop table orders")
    conn.close()


if __name__ == "__main__":
    test_create_tables()



