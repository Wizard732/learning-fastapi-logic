from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add():
    info = {"id": 2, "category": "lelee","amount": 34.2,"is_important": False} # типо json
    result = client.post("/add", json = info)

    assert result.status_code == 200

def test_delete():
    info = {"item": "admin"} # проверка админа
    result = client.delete("/clear", headers=info)

    assert result.status_code == 200
