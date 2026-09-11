from pydantic import BaseModel, Field
from lib import Response, HTTPResponse, exception_to_http_response
from service import model, view
from exception import ServErrorCode
from db import table_car as ct

class CarRegisterRequest(BaseModel):
    user_id: int = Field(...)
    make: str = Field(...)
    model: str = Field(...)
    year: int = Field(...)
    mileage: int = Field(...)
    rent_status: str = Field(...)
    min_rent_period: int = Field(...)
    max_rent_period: int = Field(...)

class CarController:
    def __init__(self):
        pass

    def register(req: CarRegisterRequest) -> HTTPResponse:
        '''
        Register a car
        '''
        car = model.Car()
        car.user_id = req.user_id
        car.make = req.make
        car.model = req.model
        car.year = req.year
        car.mileage = req.mileage
        car.rent_status = model.car.car_status_from_str(req.rent_status)
        car.min_rent_period = req.min_rent_period
        car.max_rent_period = req.max_rent_period

        resp = car.register()
        if not resp.is_success():
            return HTTPResponse(resp.code, resp.message, resp.detail)

        car = model.Car()
        car.user_id = req.user_id
        resp = car.search_for_user(car.user_id, 1)
        if isinstance(resp, Response):
            return HTTPResponse(resp.code, resp.message, resp.detail)
        elif isinstance(resp, list):
            if len(list) == 0:
                r = Response(ServErrorCode.CarRegisterFailed, "Car registers failed.")
                return HTTPResponse(r.code, r.message, r.detail)
            else:
                info = list[0]
                car_id = info.get(ct.Columns.ID, None)
                if not car_id:
                    r = Response(ServErrorCode.CarRegisterFailed, "Car registers failed for car id not defined.")
                    return HTTPResponse(r.code, r.message, r.detail)
                
                data = view.CarIdData(car_id)
                return HTTPResponse(resp.code, resp.message, resp.detail, data)