from typing import Dict
from fastapi import FastAPI, HTTPException

app = FastAPI()

users: Dict[int, Dict[str, str]] = {}
current_id = 1

# /create_user - створює нового користувача
@app.post("/create_user")
def add_user(username: str, email: str):
    global current_id
    
    for user_data in users.values():
        if user_data["email"] == email:
            raise HTTPException(
                status_code=400,
                detail="Такий користувач вже існує"
            )
    
    users[current_id] = {
        "username": username,
        "email": email
    }
    
    new_user_id = current_id
    current_id += 1

    return {
        "message": "Користувача додано",
        "user_id": new_user_id,
        "username": username,
        "email": email
    }


# /users - список всіх користувачів
@app.get("/users")
def get_all_users():
    return users


# /users/{user_id} - інформація про користувача
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    user_data = users[user_id]
    return {
        "user_id": user_id,
        "username": user_data["username"],
        "email": user_data["email"]
    }
