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

def test_stats():
    headers = {"item": "admin"}
    info = {"id": 2, "category": "lelee","amount": 34.2,"is_important": False}
    result = client.get("/stats", headers= headers )

    assert result.status_code == 200
    assert isinstance(result.json(), dict)


def test_search():
    result = client.get("/search", params = {"category": "lele"})

    assert result.status_code == 200
    assert isinstance(result.json(), list)

def test_expenses():
    result = client.get("/expenses", params={"min_price": 30.0})

    assert result.status_code == 200
    assert isinstance(result.json(),list)

def test_total():
    headers = {"item": "admin"}
    result = client.get("/total",headers= headers)

    assert result.status_code == 200
    assert isinstance(result.json(),(dict,int,float))



