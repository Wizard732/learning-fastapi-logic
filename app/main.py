from fastapi import FastAPI, HTTPException, Depends
from app.models import Expense
from app.auth import verify_admin
import json

app = FastAPI()

@app.post("/add")
async def add(item: Expense):
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f: # читаем файл
            data = json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        data = [] # если в файле не список начинаем его со списка

    if item.amount > 10000:
        item.is_important = True

    data.append(item.model_dump()) # добавляем данные в файл
    try:
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(data, f)
    except FileNotFoundError:
        return "Не удалось открыть файл"

@app.delete("/clear")
async def clear(item: str = Depends(verify_admin)):
    filename = "expenses.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump([],f) # создаем пустой файл
    return {"message":"Данные успешно удалены"}


