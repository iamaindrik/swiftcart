from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField,
    FloatField, IntegerField, TextAreaField,
    SubmitField, SelectField
)
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, URL


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Create account')


class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discount_percent = IntegerField('Discount %', validators=[Optional(), NumberRange(min=0, max=100)])
    image_url = StringField('Image URL', validators=[Optional(), URL(require_tld=False, allow_ip=True)])
    
    # ✅ New field for category
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    
    is_featured = BooleanField('Featured')
    submit = SubmitField('Save')


class SettingsForm(FlaskForm):
    store_name = StringField('Store Name', validators=[Optional()])
    brand_subtext = StringField('Brand Subtext', validators=[Optional()])
    razorpay_key_id = StringField('Razorpay Key ID', validators=[Optional()])
    razorpay_key_secret = StringField('Razorpay Key Secret', validators=[Optional()])
    submit = SubmitField('Save')


class AddressForm(FlaskForm):
    customer_name = StringField('Full Name', validators=[DataRequired()])
    customer_email = StringField('Email', validators=[DataRequired(), Email()])
    customer_phone = StringField('Phone', validators=[Optional(), Length(max=30)])
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line2 = StringField('Address Line 2', validators=[Optional()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pincode = StringField('PIN Code', validators=[DataRequired(), Length(min=4, max=10)])
    submit = SubmitField('Proceed to Pay')
