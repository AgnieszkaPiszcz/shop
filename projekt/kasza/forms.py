from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Regexp, EqualTo, ValidationError, InputRequired
from kasza.models import Customer, Category, Product
from kasza import db
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Length(min=3, max=20, message='Nazwa użytkownika musi mieć między 3 a 20 znaków.')])
    email = StringField('Adres email',
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Email(message='Podaj poprawny adres email.')])
    email_confirm = StringField('Powtórz adres email', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Email(message='Podaj poprawny adres email.'), 
                                    EqualTo('email', message='Podane adresy email się różnią.')])

    password = PasswordField('Hasło', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'),
                                    Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&-+=(),.!? "]).{8,50}$', message='Hasło musi spełniać podane kryteria.')])
    password_confirm = PasswordField('Powtórz hasło', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&-+=(),.!? "]).{8,50}$', message='Hasło musi spełniać podane kryteria.'),
                                    EqualTo('password', message='Podane hasła się różnią.')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        customer = Customer.query.filter_by(username=username.data).first()
        if customer:
            raise ValidationError('Użytkownik o tej nazwie już istnieje. Wybierz inną nazwę użytkownika.')
    
    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('Ten email jest już zajęty. Podaj inny adres email.')


class LoginForm(FlaskForm):
    email = StringField('Adres email', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Email(message='Podaj poprawny adres email.')])
    password = PasswordField('Hasło', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.')])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')


class EditAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Length(min=3, max=20, message='Nazwa użytkownika musi mieć między 3 a 20 znaków.')])
    email = StringField('Adres email',
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Email(message='Podaj poprawny adres email.')])
    address = StringField('Adres')
    submit = SubmitField('Zatwierdź')

    def validate_username(self, username):
        if username.data != current_user.username:
            customer = Customer.query.filter_by(username=username.data).first()
            if customer:
                raise ValidationError('Użytkownik o tej nazwie już istnieje. Wybierz inną nazwę użytkownika.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer:
                raise ValidationError('Ten email jest już zajęty. Podaj inny adres email.')


class AddProductForm(FlaskForm):
    name = StringField('Nazwa produktu', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'),
                                    Length(min=3, max=100, message='Nazwa produktu musi mieć między 3 a 100 znaków.')])
    price = DecimalField('Cena', validators=[InputRequired(message='To pole jest wymagane.')])
    description = TextAreaField('Opis', validators=[DataRequired(message='To pole jest wymagane.')])
    category = SelectField('Kategoria', validators=[DataRequired(message='To pole jest wymagane.')])
    pic = FileField('Zdjęcie produktu', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Nieprawidłowy format pliku. Dozwolone rozszerzenia: .jpg, .jpeg, .png.')])
    submit = SubmitField('Dodaj produkt')

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError('Produkt o tej nazwie już istnieje.')


class AddCategoryForm(FlaskForm):
    name = StringField('Nazwa kategorii', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'),
                                    Length(min=3, max=20, message='Nazwa kategorii musi mieć między 3 a 20 znaków.')])
    submit = SubmitField('Dodaj kategorię')

    def validate_name(self, name):
        product = Category.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError('Produkt o tej nazwie już istnieje.')

class EditProductForm(FlaskForm):
    name = StringField('Nazwa produktu', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'),
                                    Length(min=3, max=100, message='Nazwa produktu musi mieć między 3 a 100 znaków.')])
    price = DecimalField('Cena', validators=[DataRequired(message='To pole jest wymagane.')])
    description = TextAreaField('Opis', validators=[DataRequired(message='To pole jest wymagane.')])
    category = SelectField('Kategoria', validators=[DataRequired(message='To pole jest wymagane.')])
    pic = FileField('Zdjęcie produktu', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Nieprawidłowy format pliku. Dozwolone rozszerzenia: .jpg, .jpeg, .png.')])
    submit = SubmitField('Zatwierdź')





class AddProductToCartForm(FlaskForm):
    qty = IntegerField(validators=[
                    DataRequired(message='To pole jest wymagane.'), NumberRange(min=1, max=1000000, message=('Maksymalnie można zamówić 1000000 kg produktu.'))])
                    #Regexp('^[0-9]+$', message='Podaj poprawną ilość.')])
    submit = SubmitField('Dodaj do koszyka')

class ContactForm(FlaskForm):
    name = StringField('Imię i nazwisko', 
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Length(min=3, max=20, message='To pole musi mieć między 3 a 20 znaków.')])
    email = StringField('Adres email',
                                validators=[
                                    DataRequired(message='To pole jest wymagane.'), 
                                    Email(message='Podaj poprawny adres email.')])
    msg = TextAreaField('Treść wiadomości', validators=[DataRequired(message='To pole jest wymagane.')])
    submit = SubmitField('Wyślij wiadomość')
