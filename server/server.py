import uvicorn
from fastapi import FastAPI, HTTPException, status
from service.view import UserInfoData
from service.controller import UserLoginRequest, UserController, UserRegisterRequest
from lib import HTTPResponse

app = FastAPI(title='Car Retal System')

@app.get('/')
def root():
    return {
        "status": "success",
        "data": "Welcome to the Car Retal System"
    }

@app.post(
        '/user/login',
        status_code=status.HTTP_201_CREATED,
        response_model=HTTPResponse,
        summary='User login'
)
async def user_login(req: UserLoginRequest) -> HTTPResponse:
    return UserController().login(req)

@app.post(
    '/user/register',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='User register'
)
async def user_register(req: UserRegisterRequest) -> HTTPResponse:
    return UserController().register(req)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
