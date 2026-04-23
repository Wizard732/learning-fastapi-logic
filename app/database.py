import json
from fastapi import Depends, HTTPException
from app.auth import verify_admin
from app.models import ExpenseCreate
from app.models import ExpenseCreate


def function_add(item: ExpenseCreate):
    if item.amount > 100000:
        raise HTTPException(status_code=400, detail="Слишком большая сумма!")

    if item.amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма должна быть больше 0!")

    if item.category == "Еда" and item.amount > 500:
        item.description = "Норм"
    if item.amount == 1337:
        item.description = "Elite"

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

    if not expenses_product:
        raise HTTPException(status_code=404, detail="Трат с такой ценой не найдено")

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

def read_expenses():
    filename = "expenses.json"
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_expenses(data):
    filename = "expenses.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def function_update(id: int, updated_item: ExpenseCreate):
    data = read_expenses()
    found = False
    updated_index = -1

    for i in range(len(data)):
        if data[i]["id"] == id:
            new_data_dict = updated_item.model_dump() # Создаем словарь из новых данных
            new_data_dict["id"] = id # Сохраняем старый ID, чтобы он не пропал
            data[i] = new_data_dict # Заменяем старый объект в списке на новый
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    # Сохраняем ВЕСЬ обновленный список
    save_expenses(data)
    return data[updated_index]
