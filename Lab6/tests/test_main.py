import sys
from starlette.testclient import TestClient
from app import main
import json

client = TestClient(main.ap)

def test_ping():
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_create_item():
    response = client.post(
        "/api/tests",
        headers={"X-Token": "coneofsilence"},
        json={"id_category": 2, "status":4, "name":"тест", "description": "The Foo Barters"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "success"

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

def test_delete():
    response = client.delete("/api/tests/7")
    assert  response.status_code == 204

def test_patch():
    response = client.patch("/api/tests/8", json={"id_category":2,"status":5,"name":"test1","description":"jjjjjjjj"})
    assert response.json()["status"] == "success"