from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware, # prevent the browser problem 
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
# this should be a different database 
redis = get_redis_connection(
    host="redis-11844.c135.eu-central-1-1.ec2.cloud.redislabs.com",
    port=11844,
    password="pRdcpRkKPFn6UnEFskrDGxrmFbf5T9ER",
    decode_responses=True
)

# from redis_om import get_redis_connection, HashModel
# use the HashModel to create a database and store the data in it .
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

# get requests 
@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()
 

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)

# create a database and store the data in it . 
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

