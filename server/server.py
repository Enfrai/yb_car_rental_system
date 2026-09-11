import uvicorn
from fastapi import FastAPI, HTTPException, status
from service.view import UserInfoData
from service import view
from service import controller
from lib import HTTPResponse
from notification import NotificationCenter
from service import model

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
    '/order/book',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='Book an order'
)
async def booking_create_order(req: controller.BookingCarRequest) -> HTTPResponse:
    return controller.BookingController().book_a_car(req)

@app.post(
    '/order/all_for_users',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='search all orders for users (customer or admin)'
)
async def search_orders_for_users(req: controller.BookingHistoryRequest) -> HTTPResponse:
    return controller.BookingController().search_orders_by_user(req)

@app.post(
    '/order/confirm',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='Confirm an order'
)
async def search_orders_for_users(req: controller.BookingConfirmRequest) -> HTTPResponse:
    return controller.BookingController().confirm_order(req)


# ====================================
# ========= car management ===========
# ====================================
@app.post(
    '/car/register',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='Register a car '
)
async def car_register(req: controller.CarRegisterRequest) -> HTTPResponse:
    return controller.CarController().register(req)

@app.post(
    '/car/search',
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse,
    summary='Search cars'
)
async def car_search(req: controller.CarSearchReuest) -> HTTPResponse:
    return controller.CarController().search(req)


if __name__ == '__main__':
    notification_center = (
        NotificationCenter()
        .register(model.OnDBExitNotification())
        .register(model.OnDBExceptionNotification())
    )

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        notification_center.notify_exception()
    finally:
        notification_center.notify_exit()
