from RateCustomers import *

import pytest


def test_create_tables():
    create_tables()
    res, conn = executeQuery("select * from barcodes")
    print(res)
    conn.close()

    res, conn = executeQuery("select * from orders")
    print(res)
    conn.close()


def test_validate_barcodes():

    thing, conn = executeQuery("select sum(c) from (Select count(barcode) as c, barcode from barcodes group by barcode having c > 1)")
    dupe_num = thing[0][0]

    res, conn = executeQuery("select count(barcode) from barcodes")
    all_num = res[0][0]
    validate_barcodes()

    res, conn = executeQuery("select count(barcode) from barcodes")
    all_num_after = res[0][0]

    assert all_num_after == all_num - dupe_num

    res, conn = executeQuery(
        "select sum(c) from(Select count(barcode) as c, barcode from barcodes group by barcode having count(barcode) > 1)")
    dupe_num_after = res[0][0]
    assert dupe_num_after is None
    conn.close()

def test_get_customer_to_order():
    data = get_customer_to_order()
    res, conn = executeQuery("select count(order_id) from orders")
    # a row for each order
    assert len(data) == res[0][0]
    # no orders with no barcodes
    assert len([barcodes for cust, order, barcodes in data if barcodes == ""]) == 0

def test_get_top_customers():
    res, conn = executeQuery("select o.customer_id, count(b.barcode) from orders o, barcodes b "
                             "where b.order_id = o.order_id "
                             "group by o.customer_id "
                             "order by count(b.barcode) desc")
    expeced_top_5 = set()
    expeced_top_5.update(['10', '56', '29', '60', '59'])
    result_top_5 = set()
    result_top_5.update(get_top_five())
    assert expeced_top_5 == result_top_5

def test_get_unused_barcodes():
    '''

    '''
    res, conn = executeQuery("select * from barcodes")

    total_barcodes = len(res)

    assigned = len([barcode for barcode, order in res if order != ""])

    assert get_unused_barcodes() == total_barcodes - assigned




def test_validate_orders():

    dic, conn = executeQuery("select count(order_id) from orders o where not exists "
                "(select 1 from barcodes b where b.order_id = o.order_id )")
    num_no_barcode = dic[0][0]
    res, conn = executeQuery("select count(order_id) from orders")
    total_num = res[0][0]
    conn.close()

    validate_orders()

    res, conn = executeQuery("select count(order_id) from orders")
    total_num_after = res[0][0]

    assert total_num_after == total_num - num_no_barcode

    res, conn = executeQuery("select count(order_id) from orders o where not exists "
                "(select 1 from barcodes b where b.order_id = o.order_id )")
    num_no_barcode_after = res[0][0]
    assert num_no_barcode_after == 0
    conn.close()



if __name__ == "__main__":
    test_create_tables()
    test_validate_barcodes()
    test_validate_orders()
    test_get_customer_to_order()
    test_get_unused_barcodes()
    test_get_top_customers()
