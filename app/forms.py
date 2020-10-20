from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField

from app import MultiCheckboxField

from wtforms.validators import InputRequired, NumberRange

class SelectPriceCheck(FlaskForm):

    product = SelectField("Product", validators=[InputRequired()]) # can use models.Product.product_id for value and models.Product.product_name for label
    select = SubmitField("Select")

class NewPriceCheck(FlaskForm):

    price_check_id = StringField("Price Check ID", default=None, validators=[InputRequired()])
    product = SelectField("Product", validators=[InputRequired()]) # can use models.Product.product_id for value and models.Product.product_name for label
    supplier = SelectField("Supplier", validators=[InputRequired()]) # can use models.Supplier.supplier_id for value and models.Supplier.supplier_name for label
    url = StringField("URL", default=None, validators=[InputRequired()])
    add = SubmitField("Add")

class NewProduct(FlaskForm):

    product_id = StringField("Product ID", default=None, validators=[InputRequired()])
    product_name = StringField("Product Name", default=None, validators=[InputRequired()])
    product_type_id = SelectField("Product Type ID", default=None, validators=[InputRequired()])
    price_rrp = IntegerField("Price - RRP", default=None, validators=[InputRequired(), NumberRange(min=0)])
    price_strike = IntegerField("Price - Strike", default=None, validators=[InputRequired(), NumberRange(min=0)])
    add = SubmitField("Add")

class NewProductType(FlaskForm):
    
    product_type_id = StringField("Product Type ID", default=None, validators=[InputRequired()])
    product_type = StringField("Product Type", default=None, validators=[InputRequired()])
    add = SubmitField("Add")

class NewSupplier(FlaskForm):

    supplier_id = StringField("Supplier ID", default=None, validators=[InputRequired()])
    supplier_name = StringField("Supplier Name", default=None, validators=[InputRequired()])
    html_bs_tag = StringField("HTML (BeautifulSoup) Tag", default=None, validators=[InputRequired()])
    html_bs_attr_key = StringField("HTML (BeautifulSoup) Attribute (Key)", default=None, validators=[InputRequired()])
    html_bs_attr_value = StringField("HTML (BeautifulSoup) Attribute (Value", default=None, validators=[InputRequired()])
    add = SubmitField("Add")
