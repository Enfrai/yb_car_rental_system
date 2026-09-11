```planetuml
@startuml
title Car Rental System: Create Rental Booking

autonumber
actor "Customer" as customer
actor "Admin" as admin
participant "User" as user
participant "RentalBooking" as booking
participant "Car" as car
participant "SQLiteDatabase" as db <<Singleton>>
participant "NotificationService" as notification <<Observer>>

customer -> user : login(password, email)
activate user
user -> 
deactivate user

customer -> booking : create_booking(car_id, start_date, end_date)
activate booking

' 1. 查询车辆信息与校验
booking -> car : get_details()
activate car
car --> booking : car_info (daily_rate, min/max period)
deactivate car

' 2. 计算租车费用
booking -> car : calculate_rental_fee(duration_days)
activate car
car --> booking : total_fee
deactivate car

' 3. 通过单例获取 SQLite 连接并持久化
booking -> db : get_instance("car_rental.db")
activate db
db --> booking : db_instance
deactivate db

booking -> db : execute_non_query("INSERT INTO bookings...", params)
activate db
db --> booking : success / row_id
deactivate db

' 4. 触发观察者模式通知
booking -> booking : set_status(BookingStatus.PENDING)
booking -> booking : notify_observers("Booking PENDING confirmation")
activate booking
booking -> notification : update("Your booking request #1001 has been received.")
activate notification
notification -> notification : _send_email(customer_email)
notification --> booking : ack
deactivate notification
deactivate booking

booking --> customer : booking_confirmation_details
deactivate booking

@enduml
```