from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from market.models import User


# ---------------------------
# ✅ Register Form
# ---------------------------
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=30)])
    email_address = StringField("Email Address", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def validate_email_address(self, email_address):
        email = User.query.filter_by(email_address=email_address.data).first()
        if email:
            raise ValidationError("Email already exists.")


# ---------------------------
# ✅ Login Form
# ---------------------------
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")



# ---------------------------
# ✅ Purchase Form (simple, only submit)
# ---------------------------
class PurchaseItemForm(FlaskForm):
    submit = SubmitField("Purchase")


# ---------------------------
# ✅ Sell Form (simple, only submit)
# ---------------------------
class SellItemForm(FlaskForm):
    submit = SubmitField("Sell")
