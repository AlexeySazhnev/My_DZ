"""Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован."""

from flask import Flask, render_template, redirect, url_for
from models import db, User, RegisterForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with app.app_context():
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                            email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('register.html', form=form)


@app.route('/thank_you')
def thank_you():
    return "<h1>Thank you for registering!</h1>"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)