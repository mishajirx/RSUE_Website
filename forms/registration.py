from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, SelectField, BooleanField,SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    subject = SelectField("Предмет", choices=["Математика", "Физика", "Информатика"])
    grade = SelectField("Класс", choices=list(range(1, 12)))
    is_courier = BooleanField("Хочу быть админом")
    about = StringField('Причина запроса администраторских прав')
    submit = SubmitField('Войти')
