from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    student_id = StringField('学号', validators=[
                        DataRequired(), Length(1, 12)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    student_id = StringField('输入你的学号', validators=[
                        DataRequired(), Length(1, 12)])
    username = StringField('取个昵称', validators=[
        DataRequired(), Length(1, 64)])
    password = PasswordField('设置密码', validators=[DataRequired(),
    EqualTo('password2', message='两次输入密码必须一致')])
    password2=PasswordField('确认密码', validators=[DataRequired()])
    submit=SubmitField('注册')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该昵称已被使用.')

