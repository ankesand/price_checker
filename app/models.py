from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey

Base = declarative_base()

class Price(Base):
    
    __tablename__ = "price"

    price_id = Column("price_id", String(50), primary_key = True)
    price_check_id = Column("price_check_id", String(50), ForeignKey("price_check.price_check_id"))
    price = Column("price", Float)
    time = Column("time", DateTime())

    def __init__(self, price_id, price_check_id, price, time):

        self.price_id = price_id
        self.price_check_id = price_check_id
        self.price = price
        self.time = time

class PriceCheck(Base):
    
    __tablename__ = "price_check"

    price_check_id = Column("price_check_id", String(50), primary_key = True)
    product_id = Column("product_id", String(50), ForeignKey("product.product_id"))
    supplier_id = Column("supplier_id", String(50), ForeignKey("supplier.supplier_id"))
    url = Column("url", String(2084))
    added = Column("added", DateTime())

    def __init__(self, price_check_id, product_id, supplier_id, url, added):

        self.price_check_id = price_check_id
        self.product_id = product_id
        self.supplier_id = supplier_id
        self.url = url
        self.added = added

class Product(Base):
    
    __tablename__ = "product"

    product_id = Column("product_id", String(50), primary_key = True)
    product_name = Column("product_name", String(50))
    product_type_id = Column("product_type_id", String(50), ForeignKey("product_type.product_type_id"))
    price_rrp = Column("price_rrp", Float())
    price_strike = Column("price_strike", Float())
    
    def __init__(self, product_id, product_name, product_type_id, price_rrp, price_strike):
    
        self.product_id = product_id
        self.product_name = product_name
        self.product_type_id = product_type_id
        self.price_rrp = price_rrp
        self.price_strike = price_strike
        
class ProductType(Base):
    
    __tablename__ = "product_type"

    product_type_id = Column("product_type_id", String(50), primary_key = True)
    product_type = Column("product_type", String(50))
    
    def __init__(self, product_type_id, product_type):
    
        self.product_type_id = product_type_id
        self.product_type = product_type

class Supplier(Base):
    
    __tablename__ = "supplier"

    supplier_id = Column("supplier_id", String(50), primary_key = True)
    supplier_name = Column("supplier_name", String(50))
    html_bs_tag = Column("html_bs_tag", String(50))
    html_bs_attr_key = Column("html_bs_attr_key", String(50))
    html_bs_attr_value = Column("html_bs_attr_value", String(50))

    def __init__(self, supplier_id, supplier_name, html_bs_tag, html_bs_attr_key, html_bs_attr_value):

        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.html_bs_tag = html_bs_tag
        self.html_bs_attr_key = html_bs_attr_key
        self.html_bs_attr_value = html_bs_attr_value
