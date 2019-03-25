from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from . import main
from .forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, logout_user, current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(student_id=form.student_id.data).first()
        if user is None:
            user = User(username=form.name.data, age=form.age.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            session['old'] = form.age.data >= 40
        else:
            session['known'] = True
            session['old'] = user.age >= 40

        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False), old=session.get('old', False))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 如果提交成功就转到next页面或者回到主页面
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.student_id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        # 如果没成功提交就提示错误
        flash('无效的学号或密码')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(student_id=form.student_id.data, 
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/ineedumbrella')
def i_need_umbrella():
    latitude = jsonify(request.values.get('latitude')) # 纬度
    longitude = jsonify(request.values.get('longitude')) # 经度
    notes = jsonify(request.values.get('notes'))
    author = current_user
    is_active = True
    expire_time = jsonify(request.values.get('expire_time'))
    
@main.route('/iofferumbrella')
def i_offer_umbrella():
    latitude = jsonify(request.values.get('latitude')) # 纬度
    longitude = jsonify(request.values.get('longitude')) # 经度