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


def test_validate_barcodes():
    db = create_tables()

    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute(
        "select sum(c) from(Select count(barcode) as c, barcode from barcodes group by barcode having count(barcode) > 1)")

    dupe_num = cur.fetchone()[0]

    cur.execute("select count(barcode) from barcodes")
    all_num = cur.fetchone()[0]
    validate_barcodes(db)

    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute("select count(barcode) from barcodes")
    all_num_after = cur.fetchone()[0]

    assert all_num_after == all_num - dupe_num

    cur.execute(
        "select sum(c) from(Select count(barcode) as c, barcode from barcodes group by barcode having count(barcode) > 1)")
    dupe_num_after = cur.fetchone()
    assert dupe_num_after[0] is None


def test_validate_orders():
    db = create_tables()
    conn = db.connect("Orders.db")
    cur = conn.cursor()
    cur.execute("select count(order_id) from orders o where not exists "
                "(select 1 from barcodes b where b.order_id = o.order_id )")
    num_no_barcode = cur.fetchone()[0]
    cur.execute("select count(order_id) from orders")
    total_num = cur.fetchone()[0]
    conn.close()

    validate_orders(db)

    conn = db.connect("Orders.db")
    cur = conn.cursor()

    cur.execute("select count(order_id) from orders")
    total_num_after = cur.fetchone()[0]

    assert total_num_after == total_num - num_no_barcode

    cur.execute("select count(order_id) from orders o where not exists "
                "(select 1 from barcodes b where b.order_id = o.order_id )")
    num_no_barcode_after = cur.fetchone()[0]
    assert num_no_barcode_after == 0



if __name__ == "__main__":
    test_create_tables()
    test_validate_barcodes()
    test_validate_orders()
