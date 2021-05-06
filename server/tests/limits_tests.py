import requests
import json


def test_response_status_for_all_limits_equals_200():
    response = requests.get("http://localhost:8080/limits")
    assert response.status_code == 200


def test_response_body_for_all_limits_contains_array():
    response = requests.get("http://localhost:8080/limits")
    content = response.json()
    assert type(content) == list


def test_create_limit_with_valid_body():
    body = {
      "user_id": 124,
      "currency": "EUR",
      "country": "RUS",
      "amount": 100000
    }
    response = requests.post("http://localhost:8080/limits", data=json.dumps(body))
    assert response.status_code == 200
    assert response.json() == body


def test_create_limit_with_invalid_body():
    body = {
      "user_id": 125,
      "currency": "EUR",
      "country": "RUS",
      "amount": -100000
    }
    response = requests.post("http://localhost:8080/limits", data=json.dumps(body))
    assert response.status_code == 400
    assert response.json() == {'error': 'invalid body'}


def test_get_non_exists_limit():
    response = requests.get("http://localhost:8080/limit/125")
    assert response.status_code == 404
    assert response.json() == {'error': 'not found'}


def test_create_additional_limit_with_valid_body():
    body = {
      "user_id": 126,
      "currency": "EUR",
      "country": "RUS",
      "amount": 100000
    }
    response = requests.post("http://localhost:8080/limits", data=json.dumps(body))
    assert response.status_code == 200
    assert response.json() == body


def test_delete_additional_limit():
    body = {
      "user_id": 126,
      "currency": "EUR",
      "country": "RUS",
      "amount": 100000
    }
    response = requests.delete("http://localhost:8080/limit/126", data=json.dumps(body))
    assert response.status_code == 200
    assert response.json() == body


def test_update_limit_with_invalid_amount():
    body = {
      "currency": "EUR",
      "country": "RUS",
      "amount": -150000
    }
    response = requests.put("http://localhost:8080/limit/124", data=json.dumps(body))
    assert response.status_code == 400
    assert response.json() == {'error': 'invalid body'}


def test_update_limit_with_invalid_country():
    body = {
      "currency": "EUR",
      "country": "RUSSS",
      "amount": 150000
    }
    response = requests.put("http://localhost:8080/limit/124", data=json.dumps(body))
    assert response.status_code == 400
    assert response.json() == {'error': 'invalid body'}


def test_update_limit_with_invalid_currency():
    body = {
      "currency": "EUSER",
      "country": "RUS",
      "amount": 150000
    }
    response = requests.put("http://localhost:8080/limit/124", data=json.dumps(body))
    assert response.status_code == 400
    assert response.json() == {'error': 'invalid body'}


def test_update_limit_with_valid_body():
    body = {
      "currency": "EUR",
      "country": "RUS",
      "amount": 150000
    }
    response = requests.put("http://localhost:8080/limit/124", data=json.dumps(body))
    assert response.status_code == 200
    body["user_id"] = 124
    assert response.json() == body


def test_create_valid_transaction():
    body = {
        "user_id": 124,
        "date": "2020-01-01 08:15:27.243860",
        "currency": "EUR",
        "country": "RUS",
        "amount": 2000
    }
    response = requests.post("http://localhost:8080/transaction", json=body)
    assert response.status_code == 200
    assert response.json() == body


def test_create_invalid_amount_transaction():
    body = {
        "user_id": 124,
        "date": "2020-01-01 08:15:27.243860",
        "currency": "EUR",
        "country": "RUS",
        "amount": -1000
    }
    response = requests.post("http://localhost:8080/transaction", json=body)
    assert response.status_code == 400
    assert response.json() == {'error': 'unavailable amount'}


def test_delete_limit():
    body = {
      "user_id": 124,
      "currency": "EUR",
      "country": "RUS",
      "amount": 150000
    }
    response = requests.delete("http://localhost:8080/limit/124", data=json.dumps(body))
    assert response.status_code == 200
    assert response.json() == body

