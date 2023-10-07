from fastapi.testclient import TestClient
from app import app, UsersResponse, settings, get_db, Base,create_access_token, Products

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pytest

MYSQL_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(MYSQL_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():

    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]= override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email":"edbert@gmail.com","password":"edbert"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_products(test_user, session):
    products_data = [{
        "name":"susu",
        "price":"4000",
        "is_sale":True,
        "inventory":"10",            
        "buyer_id":test_user['id'],            
    },{
        "name":"keju",
        "price":"9000",
        "is_sale":True,
        "inventory":"50",            
        "buyer_id":test_user['id'],            
    },{
        "name":"tomat",
        "price":"2000",
        "is_sale":False,
        "inventory":"0",            
        "buyer_id":test_user['id'],            
    }]

    def create_product_model(product):
        return Products(**product)

    product_map = map(create_product_model, products_data)
    products = list(product_map)

    session.add_all(products)

    # session.add_all([Products(            
    #     "name":"susu",
    #     "price":"4000",
    #     "is_sale":"1",
    #     "inventory":"10",            
    #     "buyer_id":test_user['id'] ),
    # Products(
    #     "name":"keju",
    #     "price":"9000",
    #     "is_sale":"1",
    #     "inventory":"50",            
    #     "buyer_id":test_user['id'] ),
    # Products(
    #     "name":"tomat",
    #     "price":"2000",
    #     "is_sale":"0",
    #     "inventory":"0",            
    #     "buyer_id":test_user['id'])              
    #     ])

    session.commit()
    session.query(Products).all()

    products = session.query(Products).all()
    return products