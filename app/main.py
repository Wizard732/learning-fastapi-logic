from fastapi import FastAPI,Depends
from app.models import Expense, ExpenseCreate
from app.auth import verify_admin
import json

app = FastAPI()

@app.post("/add")
async def add(item: ExpenseCreate):
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f: # читаем файл
            data = json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        data = [] # если в файле не список начинаем его со списка

    if not data:
        new_id = 1 #если айди нету в json создаем айди 1
    else:
        new_id = data[-1]["id"] + 1 # если айди есть прибавляем +1
    new_expense = item.model_dump()
    new_expense["id"] = new_id

    if item.amount > 10000:
        new_expense['is_important'] = True

    data.append(new_expense) # добавляем данные в файл
    try:
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(data, f)
    except FileNotFoundError:
        return "Не удалось открыть файл"
    return new_expense

@app.delete("/clear")
async def clear(item: str = Depends(verify_admin)):
    filename = "expenses.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump([],f) # создаем пустой файл
    return {"message":"Данные успешно удалены"}


@app.get("/stats")
async def stats(admin: str = Depends(verify_admin)):
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f: # читаем файл
            data = json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        data = []

    stats = {}

    for expense in data:
        cat = expense["category"]
        amt = expense['amount']
        if cat in stats:
            stats[cat] += amt
        else:
            stats[cat] = amt
    return stats
