from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/', response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    for user in users:
        if int(user.id) == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}', response_class=HTMLResponse)
async def new_user(
        request: Request,
        username: Annotated[str, Path(description="Enter username")],
        age: Annotated[int, Path(description="Enter age")]
):
    new_user_id = max(user.id for user in users) + 1 if users else 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.put('/user/{user_id}/{username}/{age}', response_class=HTMLResponse)
async def update_user(
        request: Request,
        user_id: int,
        username: Annotated[str, Path(description="Enter username")],
        age: Annotated[int, Path(description="Enter age")]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return templates.TemplateResponse('users.html', {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}', response_class=HTMLResponse)
async def delete_user(request: Request, user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return templates.TemplateResponse('users.html', {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='User not found')
# python -m uvicorn module_16_5:app
