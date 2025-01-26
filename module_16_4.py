from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def new_user(user: User, username: Annotated[str, Path(description="Enter username")],
                   age: Annotated[int, Path(description="Enter age")]) -> str:
    new_user_id = users[len(users)-1].id+1 if users else 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    print (user)
    return f'User {new_user_id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: Annotated[str, Path(description="Enter username")],
                      age: Annotated[int, Path(description="Enter age")]) -> str:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return f'The user {user_id} is updated'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        for i, user in enumerate(users):
            if user.id == user_id:
                del users[i]
        return f'User {user_id} has been deleted'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')
