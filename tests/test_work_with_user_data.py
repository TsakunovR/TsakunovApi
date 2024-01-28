import json

import httpx
import allure
import pytest
import datetime
from jsonschema import validate
from core.contracts import SUCCESSFULL_LOGIN_SCHEMA

BASE_URL = 'https://reqres.in/api/users'
LOGIN_URL = 'https://reqres.in/api/login'


@allure.suite('Проверка запросов для работы с пользователями')
@allure.title('Метод удаляющий пользователя')
def test_user_delete():
    with allure.step('Выполняем DELETE запрос'):
        response = httpx.delete(BASE_URL + '/366')

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 204


json_file = open('./users_credentials.json')
users_credentials = json.load(json_file)


@pytest.mark.parametrize("user_credentials", users_credentials)
def test_create_user(user_credentials):
    headers = {'Content-Type': 'application/json'}
    response = httpx.post(BASE_URL, json=user_credentials, headers=headers)
    response_date = response.json()['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.utcnow())

    assert response_date[0:16] == current_date[0:16]


def test_successfull_login():
    users_login_password = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    headers = {'Content-Type': 'application/json'}
    response = httpx.post(LOGIN_URL, json=users_login_password, headers=headers)
    assert response.status_code == 200
    validate(response.json(), SUCCESSFULL_LOGIN_SCHEMA)

def test_login_missing_password():
    users_login_password = {
        "email": "eve.holt@reqres.in"
    }
    headers = {'Content-Type': 'application/json'}
    response = httpx.post(LOGIN_URL, json=users_login_password, headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'

def test_login_wrong_login():
    users_login_password = {
        "email": "eve.holt@reqrfes.in",
        "password": "ciica"
    }
    headers = {'Content-Type': 'application/json', "token":"sdfsdf"}
    response = httpx.post(LOGIN_URL, json=users_login_password, headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == 'user not found'