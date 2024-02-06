"""Задача 7.
Создать страницу, на которой будет форма для ввода числа
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с результатом, где будет
выведено введенное число и его квадрат.
"""
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('square'))
    return render_template('your_number.html')


@app.route('/square/', methods=['POST'])
def square():
    num = int(request.form.get('number'))
    return f"<h1>Ваше число {num},его квадрат равен {num ** 2}</h1>"


if __name__ == '__main__':
    app.run(debug=True)
