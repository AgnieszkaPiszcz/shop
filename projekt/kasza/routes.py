import secrets
import os
from flask import request, render_template, url_for,flash, redirect, jsonify, make_response
from kasza import app, db, bcrypt
from kasza.forms import AddCategoryForm, AddProductForm, EditAccountForm, RegistrationForm, LoginForm, AddProductToCartForm, EditProductForm, ContactForm
from kasza.models import Customer, Category, Product, Order, OrderItem
from flask_login import login_user, current_user, logout_user, login_required
from functools import partial


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def index():
    product_category = request.args.get('category_id')
    if product_category:
        products = Product.query.join(Product.category, aliased=True).filter_by(id=product_category) 
    else:
        products = Product.query.all()
    return render_template('index.html', products=products, categories = Category.query.all())

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(customer)
        db.session.commit() 
        flash(f'Konto {form.username.data} zostało utworzone.', 'success')
        return redirect(url_for('login'))
    print(form.errors)
    return render_template('register.html', title='Rejestracja', form=form, categories = Category.query.all())

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Witaj Kaszojadzie!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Błędne dane logowania. Spróbuj ponownie.', 'danger')
    return render_template('login.html', title='Logowanie', form=form, categories = Category.query.all()) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = EditAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        db.session.commit()
        flash(f'Dane Zostały zaktualizowane.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
    return render_template('account.html', title='account', form=form, categories = Category.query.all()) 

@app.route("/cart")
@login_required
def cart():
    curr_order = Order.query.filter_by(customer_id=current_user.id, is_completed=0).first()
    sum = 0
    order_items=[]
    if curr_order:
        order_items = OrderItem.query.filter_by(order_id=curr_order.id) 
        for item in order_items:
            sum += item.qty * item.product.price
        curr_order.sum = sum
        db.session.commit()
    return render_template('cart.html', title='cart', sum=sum, order=curr_order, order_items=order_items, categories = Category.query.all()) 

@app.route("/remove_from_cart")
@login_required
def remove_from_cart():
    item_id = request.args.get('item_id')
    order_item = OrderItem.query.filter_by(id=item_id).first()
    order = Order.query.join(Order.order_items, aliased=True).filter_by(id=order_item.id).first()
    if order_item.order.customer_id == current_user.id:
        db.session.delete(order_item)
        db.session.commit()
        flash(f'Usunięto {order_item.product.name} z koszyka.', 'success')
        if not order.order_items:
            db.session.delete(order)
            db.session.commit()
    return redirect(url_for('cart'))

@app.route("/place_order")
@login_required
def place_order():
    order_id = request.args.get('order_id')
    order = Order.query.filter_by(id=order_id).first()
    if order.customer_id == current_user.id:
        order.is_completed = 1
        db.session.commit()
        flash(f'Zamówienie zostało złożone.', 'success')
        return redirect(url_for('orders'))
    return redirect(url_for('cart'))

@app.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(customer_id=current_user.id, is_completed=1).order_by(Order.odate.desc())
    return render_template('orders.html', title='account', orders=orders, categories = Category.query.all()) 

@app.route("/product", methods=['GET', 'POST'])
def product():
    product_id = request.args.get('product_id')
    product = Product.query.filter_by(id = product_id).first()
    form = AddProductToCartForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            curr_order = Order.query.filter_by(customer_id=current_user.id, is_completed=0).first()
            if not curr_order:
                curr_order = Order(customer_id=current_user.id, is_completed=0)
                db.session.add(curr_order)
                db.session.commit()
            order_item = OrderItem(order_id = curr_order.id, product_id = product.id, qty = form.qty.data)
            db.session.add(order_item)
            db.session.commit()
            flash(f'Produkt {product.name} w ilości {order_item.qty} kg został dodany do koszyka.', 'success')
            return redirect(url_for('product', product_id=product.id))
    return render_template('product.html', title='Produkt', product=product, form=form, categories = Category.query.all()) 

def save_pic(form_pic):
    random_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_name = random_name + f_ext
    pic_path = os.path.join(app.root_path, 'static/product_pics', pic_name)
    form_pic.save(pic_path)
    return pic_name

@app.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.is_admin:
        categories = Category.query.all()
        choices = []
        for cat in categories:
            choices.append(cat.name)
        pform = AddProductForm()
        pform.category.choices = choices
        if pform.validate_on_submit():
            cat = Category.query.filter_by(name=pform.category.data).first()
            product = Product(name=pform.name.data, price=pform.price.data, description=pform.description.data, category_id=cat.id)
            if pform.pic.data:
                pic_file = save_pic(pform.pic.data)
                product.image_file = pic_file
            db.session.add(product)
            db.session.commit()
            flash(f'Produkt {product.name} został dodany.', 'success')
            return redirect(url_for('product', product_id=product.id))
        return render_template('add_product.html', title='Produkt', pform=pform, categories = Category.query.all())

@app.route("/add_category", methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.is_admin:
        cform = AddCategoryForm()
        if cform.validate_on_submit():
            cat = Category(name=cform.name.data)
            db.session.add(cat)
            db.session.commit()
            flash(f'Kategoria {cat.name} została dodana.', 'success')
            return redirect(url_for('add_category'))
        return render_template('add_category.html', title='Produkt', cform=cform, categories = Category.query.all()) 


@app.route("/edit_product", methods=['GET', 'POST'])
@login_required
def edit_product():
    if current_user.is_admin:
        categories = Category.query.all()
        choices = []
        for cat in categories:
            choices.append(cat.name)
        pform = EditProductForm()
        pform.category.choices = choices
        product_id = request.args.get('product_id')
        product = Product.query.filter_by(id = product_id).first()
        if pform.validate_on_submit():
            cat = Category.query.filter_by(name=pform.category.data).first()
            if pform.pic.data:
                pic_file = save_pic(pform.pic.data)
                product.image_file = pic_file
            if product.name != pform.name.data:
                product.name = pform.name.data
            product.price = pform.price.data
            product.description = pform.description.data
            product.category_id = cat.id
            db.session.commit()
            flash(f'Produkt {product.name} Został zaktualizowany.', 'success')
            return redirect(url_for('product', product_id=product.id))
        elif request.method == 'GET':
            cat = Category.query.join(Category.products, aliased=True).filter_by(id=product_id).first()
            pform.name.data = product.name
            pform.price.data = product.price
            pform.description.data = product.description
            pform.category.data = cat.name
        return render_template('edit_product.html', title='Produkt', pform=pform, product=product, categories = Category.query.all()) 

@app.route("/delete_product", methods=['GET', 'POST'])
@login_required
def delete_product():
    if current_user.is_admin:
        product_id = request.args.get('product_id')
        product = Product.query.filter_by(id=product_id).first()
        db.session.delete(product)
        db.session.commit()
        flash(f'Produkt {product.name} Został usunięty.', 'success')
        return redirect(url_for('index'))

@app.route("/delete_category", methods=['GET', 'POST'])
@login_required
def delete_category():
    if current_user.is_admin:
        cat_id = request.args.get('category_id')
        cat = Category.query.filter_by(id=cat_id).first()
        product = Product.query.join(Product.category, aliased=True).filter_by(id=cat.id).first()
        if product:
            flash(f'Nie można usunąć kategorii, do której przypisane są produkty.', 'danger')
            return redirect(url_for('add_category'))
        else:
            db.session.delete(cat)
            db.session.commit()
            flash(f'Kategoria {cat.name} Została usunięta.', 'success')
            return redirect(url_for('add_category'))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate():
            return make_response(jsonify({'message': 'validated'}), 200)
        return make_response(jsonify(form.errors))
    elif request.method == 'GET' and current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email
    return render_template('contact.html', title='Kontakt', form=form, categories = Category.query.all()) 

@app.route("/contact/send_email", methods=['GET', 'POST'])
def send_email():
    res = make_response(jsonify({'message': 'send_email'}), 200)
    return res

@app.route("/about")
def about():
    return render_template('about.html', categories = Category.query.all()) 



