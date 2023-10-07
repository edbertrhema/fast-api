from app import UsersResponse, Token , settings
from jose import jwt
# from .database import client, session

import pytest




# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'hello world docker'

def test_create_user(client):
    res = client.post("/users/",json={"email": "hai@gmail.com", "password":"hai"})
    
    new_user = UsersResponse(**res.json())
    assert new_user.email == "hai@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login/",data={"username":test_user['email'], "password": test_user['password']})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com','tamara',403),
    ('tamara@gmail.com','wrongpassword',403),
    ('wrongemail@gmail.com','wrongpassword',403),
    (None,'tamara',422),
    ('tamara@gmail.com',None,422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'