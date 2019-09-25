


begin transaction

---Constraints:
---order_id is unique
---no order without barcode
create table orders 
(
	order_id int primary key,
	customer_id int not null
)
ALTER TABLE orders 
  ADD CONSTRAINT chkNoOrderWithoutBarcode 
  CHECK (dbo.CheckFunction(order_id) = 1); 

---Constraints:
---no duplicate barcode
---order_id can be empty
create table barcodes 
(
	barcode nvarchar primary key,
	order_id int references orders null  -- constraint would need to be deferred when inserting rows
)

ALTER TABLE orders 
  ADD CONSTRAINT chkNoOrderWithoutBarcode
  CHECK (dbo.CheckFunction(order_id) = 1);
go

create function dbo.CheckFunction(@order_id int)
returns int
as begin
	if exists (select 1 from barcodes b where @order_id = b.order_id )
		return (select 1)
	return 0
end

---note use of primary keys creates indexes


 