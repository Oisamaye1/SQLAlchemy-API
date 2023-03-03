from app import app, db, ma
from flask import render_template, request, redirect, flash, url_for, Response
from sqlalchemy.inspection import inspect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class Products(db.Model):
  __tablename__ = "users"
  id = db.Column('student_id', db.Integer, primary_key = True)
  name = db.Column("name",  db.String(40))
  description = db.Column("description",  db.String(40))
  quantity = db.Column("quatity", db.Integer())
  price = db.Column("price", db.Float)
  photo = db.Column("image", db.Text)

def __init__(self, name, description, quantity, price, photo):
   self.name = name
   self.description = description
   self.quantity = quantity
   self.price = price
   self.photo = photo

class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'quantity', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class Product(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Product Description', validators=[DataRequired(), Length(max=150)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), Length(max=10)])
    price = FloatField('Price', validators=[DataRequired(), Length(max=10)])
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
def index():
  form=Product()

  if request.method == "POST":
    pic = form.photo.data
    new_product = Products(name = form.name.data, description=form.description.data, quantity=form.quantity.data, price=form.price.data, photo=pic.read())
    db.session.add(new_product)
    db.session.commit()
    return redirect(request.url)

  return render_template("index.html", form=form)


@app.route("/products", methods=["GET", "POST"])
def get_products():
  all_products = Products.query.all()
  products = products_schema.dump(all_products)
  return render_template("products.html", all_products=all_products,  products=products)


@app.route("/products/<id>", methods=["GET", "POST"])
def get_product(id):
  product = Products.query.get(id)
  single_product = product_schema.dump(product)
  return render_template("product.html", product=product, single_product=single_product)

@app.route("/products/<id>/image", methods=["GET", "POST"])
def image(id):
  product = Products.query.get(id)
  return Response(product.photo) 

@app.route("/products/<id>/update-product", methods=["GET", "POST"])
def update_product(id):
  form=Product()
  product = Products.query.get(id)

  if request.method == "POST":
    name = form.name.data
    description=form.description.data
    quantity=form.quantity.data
    price=form.price.data
    photo=form.photo.data

    product.name = name
    product.description = description
    product.quantity = quantity
    product.price = price
    product.photo = photo
    db.session.commit()
    return redirect(request.url)

  return render_template("update.html", product=product, form=form)

@app.route("/products/<id>/delete-product")
def delete_product(id):
  product = Products.query.get(id)
  db.session.delete(product)
  db.session.commit()
  return redirect(url_for("get_products"))

