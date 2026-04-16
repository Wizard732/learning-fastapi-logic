from pydantic import Field, BaseModel

class Expense(BaseModel):
    id: int = Field(gt=0)
    category: str = Field(min_length=3, max_length=20)
    amount: float = Field(gt=0)
    is_important: bool = Field(default=False)

class ExpenseCreate(BaseModel):
    category: str = Field(min_length=3, max_length=20)
    amount: float = Field(gt=0)
    is_important: bool = Field(default=False)
    