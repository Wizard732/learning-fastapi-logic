import json
from fastapi import Depends, HTTPException
from app.auth import verify_admin
from app.models import ExpenseCreate


def function_add(item: ExpenseCreate):
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f:  # читаем файл
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # если в файле не список начинаем его со списка

    if not data:
        new_id = 1  # если айди нету в json создаем айди 1
    else:
        new_id = data[-1]["id"] + 1  # если айди есть прибавляем +1
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


def function_clear(item: str):
    filename = "expenses.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump([],f) # создаем пустой файл
    return {"message":"Данные успешно удалены"}


def function_stats(admin: str):
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


def function_search(category:str):
    filtered_expenses = []
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"message":"Данные не удалось прочитать"}

    for item in data:
        if item["category"] == category: # если элемент равен тому который ищем добавляем в список
            filtered_expenses.append(item)

    if not filtered_expenses:
        raise HTTPException(status_code=404, detail="Ничего не найдено")

def function_expenses(min_price: float):
    expenses_product = []
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"message":"Данные не удалось прочитать"}

    for item in data:
        if item["amount"] >= min_price: # если элемент равен или больше тому который ищем добавляем в список
            expenses_product.append(item)
        raise HTTPException(status_code=400, detail="Элемент меньше нужного значения")
    return expenses_product


def function_total(admin: str):
    filename = "expenses.json"
    total_sum = 0

    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return "Не удалось прочитать файл"

    for item in data:
        total_sum += item["amount"] # добавляем в тотал сум сумму с каждой записи в json
    return {"total_sum": total_sum}


def function_delete(id: int, admin: str):
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "Не удалось открыть файл"}

    new_data = []
    for item in data:
        if item["id"] != id:
            new_data.append(item)

    if len(new_data) == len(data):  # если длина нового списка такая же то айди не найдет
        return {"message": "Запись с таким ID не найдена"}

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)  #
    return {"message": f"Запись с id {id} успешно удалена"}  # добавляем старые айди кроме того который нужно удалить