import databases
import sqlalchemy
import random
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

DATABASE_URL = "sqlite:///shop.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String)
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("order_state", sqlalchemy.Boolean)
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float)
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class Order(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime
    order_state: bool

class Product(BaseModel):
    name: str
    description: str
    price: float

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users", response_model=User)
async def create_user(user: User):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.get("/users", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 25):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)  
async def get_user(id: int):
    query = users.select().where(users.c.id == id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(id: int, user: User):
    query = users.update().where(users.c.id == id).values(**user.dict())
    await database.execute(query)
    return {**user.dict(), "id": id}

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(id: int):
    query = users.delete().where(users.c.id == id)
    await database.execute(query)
    return {"message": "user deleted"}

@app.post("/orders", response_model=User)
async def create_order(order: Order):
    query = orders.insert().values(user_id=order.user_id, product_id=order.product_id, order_date=order.order_date, order_state=order.order_state)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}

@app.get("/orders", response_model=List[Order])
async def get_orders(skip: int = 0, limit: int = 25):
    query = orders.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(id: int):
    query = orders.select().where(orders.c.id == id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return order

@app.get("/orders/{user_id}", response_model=List[Order])
async def get_orders_by_user_id(id: int):
    query = orders.select().where(users.c.id == id)
    order = await database.fetch_all(query)
    if order is None:
        raise HTTPException(status_code=404, detail="orders not found")
    return order

@app.get("/orders/{product_id}", response_model=List[Order])
async def get_orders_by_product_id(id: int):
    query = orders.select().where(products.c.id == id)
    order = await database.fetch_all(query)
    if order is None:
        raise HTTPException(status_code=404, detail="orders not found")
    return order

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(id: int, order: Order):
    query = orders.update().where(orders.c.id == id).values(**order.dict())
    await database.execute(query)
    return {**order.dict(), "id": id}

@app.delete("/orders/{order_id}", response_model=Order)
async def delete_order(id: int):
    query = orders.delete().where(orders.c.id == id)
    await database.execute(query)
    return {"message": "order deleted"}

@app.post("/products", response_model=Product)
async def create_products(product: Product):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}

@app.get("/products", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 25):
    query = products.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

@app.get("/products/{product_id}", response_model=Product)
async def get_product(id: int):
    query = products.select().where(products.c.id == id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(id: int, product: Product):
    query = products.update().where(products.c.id == id).values(**product.dict())
    await database.execute(query)
    return {**product.dict(), "id": id}

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(id: int):
    query = products.delete().where(products.c.id == id)
    await database.execute(query)
    return {"message": "product deleted"}

# the code block below this comment is responsible for generating data in the database

# @app.post("/generate_users/{count}")
# async def generate_users(count: int):
#     for i in range(count):
#         query = users.insert().values(name=f"user{i*10}", surname=f"family{i*10}", email=f"mail{i}@mail.ru", password="".join([str(digit) for digit in range(10)]))
#         await database.execute(query)
#     return {"message": f"{count} users generated"}

# @app.post("/generate_orders/{count}")
# async def generate_orders(count: int):
#     for i in range(count):
#         query = orders.insert().values(user_id=random.randint(0, 25), product_id=random.randint(0, 35), order_date=datetime.now(), order_state=False)
#         await database.execute(query)
#     return {"message": f"{count} orders generated"}

# @app.post("/generate_products/{count}")
# async def generate_products(count: int):
#     for i in range(count):
#         query = products.insert().values(name="".join([chr(code) for code in range(ord('a'), ord('z') + 1)]) + str(i*10), description="".join([chr(code) for code in range(ord('z'), ord('a') - 1, -1)]) + str(i*10), price=round(random.uniform(0.10, 100), 2))
#         await database.execute(query)
#     return {"message": f"{count} products generated"}