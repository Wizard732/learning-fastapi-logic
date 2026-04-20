from fastapi import FastAPI,Depends, HTTPException
from app.models import Expense, ExpenseCreate
from app.auth import verify_admin
from app.database import (function_add, function_clear, function_stats, function_search, function_expenses,
function_total, function_delete)
import json

app = FastAPI()

@app.post("/add")
async def add(item: ExpenseCreate):
    return function_add(item)

@app.delete("/clear")
async def clear(item: str = Depends(verify_admin)):
    return function_clear(item)



@app.get("/stats")
async def stats(admin: str = Depends(verify_admin)):
    return function_stats(admin)


@app.get("/search")
async def search(category: str):
    return function_search(category)

@app.get("/expenses")
async def expenses(min_price: float):
    return function_expenses(min_price)


@app.get("/total")
async def total(admin: str = Depends(verify_admin)):
    return function_total(admin)

@app.delete("/delete")
async def delete(id: int, admin: str = Depends(verify_admin)):
    return function_delete(id,admin)