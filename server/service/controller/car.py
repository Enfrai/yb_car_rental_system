from pydantic import BaseModel, Field
from lib import Response, HTTPResponse, exception_to_http_response
from service import model, view
from exception import ServErrorCode
from db import table_car as ct

class CarRegisterRequest(BaseModel):
    user_id: str = Field(...)
    make: str = Field(...)
    model: str = Field(...)
    year: int = Field(...)
    mileage: int = Field(...)
    rent_status: str = Field(...)
    min_rent_period: int = Field(...)
    max_rent_period: int = Field(...)

class CarSearchReuest(CarRegisterRequest):
    limit: int = Field(...)
    car_id: str = Field(...)

class CarController:
    def __init__(self):
        pass

    def search(self, req: CarSearchReuest) -> HTTPResponse:
        '''
        Search cars by customized conditions
        '''
        try:
            car = model.Car()
            car.car_id = int(req.car_id) if req.car_id else None
            car.user_id = int(req.user_id) if req.user_id else None
            car.make = req.make
            car.model = req.model
            car.year = req.year
            car.mileage = req.mileage
            car.rent_status = req.rent_status

            resp = car.search_with_conditions()
            if isinstance(resp, Response):
                return HTTPResponse(resp.code, resp.message, resp.detail)
            elif isinstance(resp, list):
                all = []
                for e in resp:
                    one = view.CarInfoData().build(
                        car.car_id, car.user_id, car.make, car.model, car.year, car.mileage, car.rent_status, car.min_rent_period, car.max_rent_period
                    )
                    all.append(one)
                r = Response(ServErrorCode.Success)
                return HTTPResponse(r.code, r.message, r.detail, view.CarInfoList().build(all))
            else:
                r = Response(ServErrorCode.CommonError, 'Search error')
                return HTTPResponse(r.code, r.message, r.detail)
        except ValueError:
            r = Response(ServErrorCode.CommonError, 'Invalid id')
            return HTTPResponse(r.code, r.message, r.detail)

    def register(self, req: CarRegisterRequest) -> HTTPResponse:
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