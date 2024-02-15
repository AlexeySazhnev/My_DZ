"""Необходимо создать API для управления списком автомобилей. Каждый автомобиль должен
содержать марку и описание. Для каждого авто должна быть возможность
указать статус (на ходу/в ремонте).
API должен содержать следующие конечные точки:
○ GET /cars - возвращает список всех автомобилей.
○ GET /cars/{id} - возвращает автомобиль с указанным идентификатором.
○ POST /cars - добавляет новый автомобиль.
○ PUT /cars/{id} - обновляет авто с указанным идентификатором.
○ DELETE /cars/{id} - удаляет авто с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и
ответа. Для этого использовать библиотеку Pydantic."""
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Список автомобилей автосервиса",
        version="15.02.2024",
        description="Личная документация сервиса",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()
app.openapi = custom_openapi


class Car(BaseModel):
    id: int
    brand: str
    description: str
    status: str


cars = [
    {"id": 1, "brand": "Mercedes", "description": "red", "status": "it is working properly"},
    {"id": 2, "brand": "VAZ", "description": "green", "status": "under repair"},
    {"id": 3, "brand": "Hyundai", "description": "white", "status": "it is working properly"},
]


@app.get("/")
async def list_cars():
    return cars


@app.get("/cars/{id}")
async def cars_id(id: int):
    for car in cars:
        if car["id"] == id:
            return car
    return {"response": "There is no such car!"}


@app.post("/cars")
async def add_car(car: Car):
    cars.append(car)
    return cars


@app.put("/change_car")
async def change_car(car: Car):
    for i in cars:
        if i["id"] == car.id:
            i["brand"] = car.brand
            i["description"] = car.description
            i["status"] = car.status
        return cars
    return {"response": "No task with this id"}


@app.delete("/cars/{id}")
async def delete_car(id: int):
    for i in range(len(cars)):
        if cars[i]["id"] == id:
            del cars[i]
        return cars
    return {"response": "There is no such car!"}