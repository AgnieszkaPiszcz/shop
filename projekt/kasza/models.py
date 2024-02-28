from datetime import datetime
from kasza import db, login_maganer
from flask_login import UserMixin


@login_maganer.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)


class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', back_populates='customer')
    is_admin = db.Column(db.Integer, nullable=True) 
    address = db.Column(db.Text)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_all_order_items(self):
        result=[]
        for order in self.orders:
            for order_item in order.order_items:
                result.append(order_item)
        return result


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float(asdecimal=True), nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default_kasza.jpg')
    description = db.Column(db.Text, nullable=False)
    order_items = db.relationship('OrderItem', back_populates='product', lazy='subquery')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products')


    def __repr__(self):
        return f"Product('{self.name}', '{self.price}', '{self.image_file}')" 


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    odate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False) 
    customer = db.relationship('Customer', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')
    sum = db.Column(db.Float(asdecimal=True))
    is_completed = db.Column(db.Integer, nullable=False) 


    def __repr__(self):
        return f"Order('{self.date}', '{self.customer_id}')"


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship('Order', back_populates='order_items')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', back_populates='order_items', lazy='subquery') 
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.order_id}', '{self.product_id}', {self.qty})"

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    products = db.relationship('Product', back_populates='category')


