from app import app
from app import session

from flask import render_template

from sqlalchemy import func, and_#, asc, desc

from app.models import Product, ProductType, Supplier, PriceCheck, Price
from app.forms import SelectPriceCheck, NewPriceCheck, NewProduct, NewProductType, NewSupplier

from datetime import datetime

@app.route("/", methods=["GET", "POST"])
@app.route("/price_checker", methods=["GET", "POST"])
def price_checker():
    
    title = "ankesand.com | price_checker"

    price_check = SelectPriceCheck()
    price_check.product.choices = [(product.product_id, product.product_name) for product in session.query(Product).all()]

    # prices_biggest_fall = _
    
    if price_check.validate_on_submit():

        product = price_check.product.data
        
        p1 = session.query(Price.price_check_id,
                           Product.product_id,
                           Product.product_name,
                           Supplier.supplier_id,
                           Supplier.supplier_name,
                           Product.price_rrp,
                           Product.price_strike,
                           PriceCheck.url,
                           func.max(Price.time).label("time_latest"),
                           func.min(Price.price).label("price_min"),
                           func.avg(Price.price).label("price_avg"),
                           func.max(Price.price).label("price_max")
                           ).\
                             group_by(Price.price_check_id).\
                             order_by(Price.price_check_id).\
                             join(PriceCheck, Price.price_check_id == PriceCheck.price_check_id).\
                             join(Product, PriceCheck.product_id == Product.product_id).\
                             join(Supplier, PriceCheck.supplier_id == Supplier.supplier_id).\
                             subquery()

        p2 = session.query(Price.price_check_id,
                           Price.time,
                           Price.price.label("price_latest")
                           ).\
                             subquery()

        query = session.query(p1, p2).join(p2, and_(p1.c.price_check_id == p2.c.price_check_id, p1.c.time_latest == p2.c.time))

        price_checks_queried = query.filter(p1.c.product_id == product).all()
        
        return render_template("price_checker.html", title = title, price_check = price_check,
                               price_checks_queried = price_checks_queried
                               )
    
    return render_template("price_checker.html", title = title, price_check = price_check)

@app.route("/price_checker/new_price_check", methods=["GET", "POST"])
def new_price_check():

    title = "ankesand.com | new price check (price checker)"

    price_check = NewPriceCheck()
    price_check.product.choices = [(product.product_id, product.product_name) for product in session.query(Product).all()]
    price_check.supplier.choices = [(supplier.supplier_id, supplier.supplier_name) for supplier in session.query(Supplier).all()]

    price_checks_all = session.query(PriceCheck).all()

    if price_check.validate_on_submit():
        
        try:
            session.add(PriceCheck(price_check.price_check_id.data,
                                   price_check.product.data,
                                   price_check.supplier.data,
                                   price_check.url.data,
                                   datetime.now()
                                   )
                        )
            session.commit()
            
            add_new_price_check_status = "Added: " + price_check.price_check_id.data

            price_checks_all = session.query(PriceCheck).all()
            
        except:
            session.rollback()
            add_new_price_check_status = "Could not add: " + price_check.price_check_id.data
            
        return render_template("new_price_check.html", title = title, price_check = price_check, price_checks_all = price_checks_all,
                               add_new_price_check_status = add_new_price_check_status
                               )
                               
    return render_template("new_price_check.html", title = title, price_check = price_check, price_checks_all = price_checks_all)

@app.route("/price_checker/new_product", methods=["GET", "POST"])
def new_product():

    title = "ankesand.com | new product (price checker)"

    product = NewProduct()
    product.product_type_id.choices = [(product_type.product_type_id,
                                        product_type.product_type
                                        ) for product_type in session.query(ProductType).order_by(ProductType.product_type).all()
                                       ]

    products_all = session.query(Product).order_by(Product.product_name).all()

    if product.validate_on_submit():
        
        try:
            session.add(Product(product.product_id.data,
                                product.product_name.data,
                                product.product_type_id.data,
                                product.price_rrp.data,
                                product.price_strike.data
                                )
                        )
            session.commit()
            
            add_new_product_status = "Added: " + product.product_name.data
            
            products_all = session.query(Product).order_by(Product.product_name).all()

        except:
            session.rollback()
            add_new_product_status = "Could not add: " + product.product_name.data
            
        return render_template("new_product.html", title = title, product = product, products_all = products_all,
                               add_new_product_status = add_new_product_status)

    return render_template("new_product.html", title = title, product = product, products_all = products_all)

@app.route("/price_checker/new_product_type", methods=["GET", "POST"])
def new_product_type():

    title = "ankesand.com | new product type (price checker)"

    product_type = NewProductType()

    product_types_all = session.query(ProductType).order_by(ProductType.product_type).all()

    if product_type.validate_on_submit():

        try:
            session.add(ProductType(product_type.product_type_id.data,
                                    product_type.product_type.data
                                    )
                        )
            session.commit()
            
            add_new_product_type_status = "Added: " + product_type.product_type.data

            product_types_all = session.query(ProductType).order_by(ProductType.product_type).all()
            
        except:
            session.rollback()
            add_new_product_type_status = "Could not add: " + product_type.product_type.data

        return render_template("new_product_type.html", title = title, product_type = product_type, product_types_all = product_types_all,
                               add_new_product_type_status = add_new_product_type_status
                               )
        
    return render_template("new_product_type.html", title = title, product_type = product_type, product_types_all = product_types_all)

@app.route("/price_checker/new_supplier", methods=["GET", "POST"])
def new_supplier():

    title = "ankesand.com | new supplier (price checker)"

    supplier = NewSupplier()
    
    suppliers_all = session.query(Supplier).all()

    if supplier.validate_on_submit():

        try:
            session.add(Supplier(supplier.supplier_id.data,
                                 supplier.supplier_name.data,
                                 supplier.html_bs_tag.data,
                                 supplier.html_bs_attr_key.data,
                                 supplier.html_bs_attr_value.data,
                                 )
                        )
            session.commit()
            
            add_new_supplier_status = "Added: " + supplier.supplier_name.data
            
            suppliers_all = session.query(Supplier).all()
            
        except:
            session.rollback()
            add_new_supplier_status = "Could not add: " + supplier.supplier_name.data
            
        return render_template("new_supplier.html", title = title, supplier = supplier, suppliers_all = suppliers_all,
                               add_new_supplier_status = add_new_supplier_status
                               )
    
    return render_template("new_supplier.html", title = title, supplier = supplier, suppliers_all = suppliers_all)

@app.route("/dummy-route")
def dummy_route():
    return "<h3>[Dummy route]</h3>"