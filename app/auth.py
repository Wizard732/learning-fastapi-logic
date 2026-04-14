from fastapi import HTTPException, Header

def verify_admin(item: str = Header(None)):
    if item != "admin":
        raise HTTPException(status_code=403,detail="Ошибка в праве доступа")



