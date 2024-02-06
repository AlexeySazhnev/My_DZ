"""Задача 4.
Создать страницу, на которой будет форма для ввода текста и
кнопка "Отправить"
При нажатии кнопки будет произведен подсчет количества слов
в тексте и переход на страницу с результатом.
"""
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('num_of_words'))
    return render_template('Home.html')


@app.route('/number_of/', methods=['POST'])
def num_of_words():
    text = request.form.get('text').split()
    return f"<h1>Количество слов в Вашем тексте {len(text)}</h1>"


if __name__ == '__main__':
    app.run(debug=True)
