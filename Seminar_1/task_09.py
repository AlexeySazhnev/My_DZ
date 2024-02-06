"""Создать базовый шаблон для интернет-магазина,
содержащий общие элементы дизайна (шапка, меню,
подвал), и дочерние шаблоны для страниц категорий
товаров и отдельных товаров.
Например, создать страницы "Одежда", "Обувь" и "Куртка",
используя базовый шаблон."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Работает'


@app.route('/clothes/')
def get_clothes():
    return render_template('clothes.html')


@app.route('/footwear/')
def get_footwear():
    return render_template('footwear.html')


@app.route('/jacket/')
def get_jacket():
    return render_template('jacket.html')


if __name__ == '__main__':
    app.run()
