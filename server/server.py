import uvicorn
from fastapi import FastAPI, HTTPException, status
from service.view import UserInfoData
from service import controller
from lib import HTTPResponse

app = FastAPI(title='Car Retal System')

# ============== test root ================

@app.get('/')
def root():
    return {
        "status": "success",
        "data": "Welcome to the Car Retal System"
    }


# ====================================
# ============== user ================
# ====================================
@app.post(
        '/user/login',
        status_code=status.HTTP_201_CREATED,
        response_model=HTTPResponse,
        summary='User login'
)
async def user_login(req: controller.UserLoginRequest) -> HTTPResponse:
    return controller.UserController().login(req)

@app.post(
    '/user/register',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='User register'
)
async def user_register(req: controller.UserRegisterRequest) -> HTTPResponse:
    return controller.UserController().register(req)

@app.post(
        '/user/update',
        status_code=status.HTTP_201_CREATED,
        response_model=HTTPResponse,
        summary='Update user infomations'
)
async def user_update(req: controller.UserUpdateRequest) -> HTTPResponse:
    return controller.UserController().update(req)

@app.post(
        '/user/search',
        status_code=status.HTTP_201_CREATED,
        response_model=HTTPResponse,
        summary='Search a specific user.'
)
async def user_search(req: controller.UserSearchRequest) -> HTTPResponse:
    return controller.UserController().search(req)


# ====================================
# ============ booking ===============
# ====================================
@app.post(
    '/booking/create_order',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='user '
)
async def booking_create_order() -> HTTPResponse:
    pass




# ====================================
# ========= car management ===========
# ====================================


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
