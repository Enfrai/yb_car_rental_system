```mermaid
@startuml
skinparam classAttributeIconSize 0
title Car Rental System

' ==================== SINGLETON PATTERN (SQLITE) ====================
abstract class Database {
    - db_file: str
    - __init__(db_file: str)
    + execute_query(query: str, params: tuple): list
    + execute_non_query(query: str, params: tuple): int
    + commit(): None
    + close(): None
}

class SQLiteDatabase extends Database {
    - connection: sqlite3.Connection
    - cursor: sqlite3.Cursor
}

class DBHelper <<Singleton>> {
    - _instance: Optional[Database]
    + static get_instance(db_file: str): Database
    + execute_query(query: str, params: tuple): list
    + execute_non_query(query: str, params: tuple): int
    + commit(): None
    + close(): None
}

' ==================== USER SYSTEM & FACTORY PATTERN ====================
abstract class User {
    # user_id: str
    # username: str
    # password_hash: str
    # email: str
    # role: str
    + login(email: str, password: str): bool
    + logout(): None
}

class Customer extends User {
    - driver_license_no: str
    + view_available_cars(db: DBHelper): list[Car]
    + create_booking(car_id: str, start_date: date, end_date: date): RentalBooking
}

class Admin extends User {
    - employee_id: str
    + add_car(car: Car, db: DBHelper): bool
    + update_car(car: Car, db: DBHelper): bool
    + delete_car(car_id: str, db: DBHelper): bool
    + approve_booking(booking_id: str): bool
    + reject_booking(booking_id: str): bool
}

abstract class UserFactory {
    + {abstract} create_user(password: str, username: str, email: str, **kwargs): User
}

class CustomerFactory extends UserFactory {
    + create_user(password: str, username: str, email: str, **kwargs): Customer
}

class AdminFactory extends UserFactory {
    + create_user(password: str, username: str, email: str, **kwargs): Admin
}

' ==================== CAR MANAGEMENT ====================
class Car {
    - car_id: str
    - make: str
    - model: str
    - year: int
    - mileage: float
    - is_available: bool
    - min_rent_period_days: int
    - max_rent_period_days: int
    - daily_rate: float

    + get_details(): dict
    + update_mileage(new_mileage: float): None
    + set_availability(status: bool): None
    + calculate_rental_fee(days: int): float
    + save_to_db(db: DBHelper): bool
}

' ==================== OBSERVER PATTERN & BOOKING ====================
interface Observer {
    + {abstract} update(message: str): None
}

class NotificationService implements Observer {
    + update(message: str): None
    - _send_email(message: str): None
}

abstract class BookingSubject {
    - _observers: list[Observer]
    + attach(observer: Observer): None
    + detach(observer: Observer): None
    + notify_observers(message: str): None
}

class RentalBooking extends BookingSubject {
    - booking_id: str
    - customer_id: str
    - car_id: str
    - start_date: date
    - end_date: date
    - total_fee: float
    - status: BookingStatus

    + calculate_fee(daily_rate: float): float
    + update_status(new_status: BookingStatus): None
    + save_to_db(db: DBHelper): bool
}

enum BookingStatus {
    PENDING
    APPROVED
    REJECTED
    COMPLETED
    CANCELLED
}

' ==================== RELATIONSHIPS ====================
Customer "1" -- "*" RentalBooking : places >
Admin "1" -- "*" RentalBooking : reviews >
Admin "1" -- "*" Car : manages >
RentalBooking "*" -- "1" Car : reserves >
RentalBooking "1" *-- "1" BookingStatus

DBHelper "1" <.. User : executes SQL via
DBHelper "1" <.. Car : executes SQL via
DBHelper "1" <.. RentalBooking : executes SQL via

@enduml
```