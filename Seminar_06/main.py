"""Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
содержать информацию о доступных товарах, их описаниях и ценах. Таблица
пользователи должна содержать информацию о зарегистрированных
пользователях магазина. Таблица заказы должна содержать информацию о
заказах, сделанных пользователями.
○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
имя, фамилия, адрес электронной почты и пароль.
○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
название, описание и цена.
○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
заказа.
Создайте модели pydantic для получения новых данных и
возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через
создание маршрутов, REST API (итого 15 маршрутов).
○ Чтение всех
○ Чтение одного
○ Запись
○ Изменение
○ Удаление"""
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, ForeignKey
from datetime import datetime


class User(BaseModel):
    id_user: int
    username: str
    surname: str
    email: str
    password: str


class Product(BaseModel):
    id_product: int
    name: str
    description: str
    price: float


class Order(BaseModel):
    id: int
    id_user: int
    id_product: int
    date: datetime
    status: str


DATABASE_URL = "sqlite:///online_store.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table("Users", metadata,
                         sqlalchemy.Column("id_user", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("username", sqlalchemy.String),
                         sqlalchemy.Column("surname", sqlalchemy.String),
                         sqlalchemy.Column("email", sqlalchemy.String),
                         sqlalchemy.Column("password", sqlalchemy.String))
products = sqlalchemy.Table("Products", metadata,
                            sqlalchemy.Column("id_product", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("name", sqlalchemy.String),
                            sqlalchemy.Column("description", sqlalchemy.String),
                            sqlalchemy.Column("price", sqlalchemy.Numeric))
orders = sqlalchemy.Table("Orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("id_product", sqlalchemy.Integer, ForeignKey('Products.id_product')),
                          sqlalchemy.Column("id_user", sqlalchemy.Integer, ForeignKey('Users.id_user')),
                          sqlalchemy.Column("date", sqlalchemy.DateTime, default=datetime.utcnow),
                          sqlalchemy.Column("status", sqlalchemy.String))
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Crud для пользователей
@app.get("/users/", response_model=list[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id_user == user_id)
    return await database.fetch_one(query)


@app.post("/users/", response_model=User)
async def create_user(user: User):
    query = users.insert().values(username=user.username, surname=user.surname, email=user.email,
                                  password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id_user": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: User):
    query = users.update().where(users.c.id_user == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id_user": user_id}


@app.delete("/users/{user_id}/")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id_user == user_id)
    await database.execute(query)
    return {"message": "Удаление успешно!!!"}


# Crud для товаров
@app.get("/products/", response_model=list[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id_product == product_id)
    return await database.fetch_one(query)


@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id_product": last_record_id}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    query = products.update().where(products.c.id_product == product_id).values(**product.dict())
    await database.execute(query)
    return {**product.dict(), "id_product": product_id}


@app.delete("/products/{product_id}/")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id_product == product_id)
    await database.execute(query)
    return {"message": "Удаление успешно!!!"}


# Crud для заказов
@app.get("/orders/", response_model=list[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    query = orders.insert().values(id=order.id, id_product=order.id_product, id_user=order.id_user,
                                   date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: Order):
    query = orders.update().where(orders.c.id == order_id).values(**order.dict())
    await database.execute(query)
    return {**order.dict(), "id": order_id}


@app.delete("/orders/{order_id}/")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": "Удаление успешно!!!"}
