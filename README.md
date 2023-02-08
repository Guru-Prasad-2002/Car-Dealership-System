# Car Dealership System

A web-based car dealership system built using Flask, Flask-SQLAlchemy, and Bootstrap. This system helps manage the car dealership's cars, customers, showrooms, managers, and sales.

## Getting Started

1. Clone the repository
2. Run `pip install -r Requirements.txt` to install dependencies
3. Run `python app.py` to start the server
4. Navigate to `localhost:5000` in your browser
5. Login with the following credentials:
   - Username: admin
   - Password: password

## Tables

The system consists of five tables:

- Car: includes car_id, model, year, color, price, and quantity
- Customer: includes customer_id, name, address, and phone
- Showroom: includes showroom_id, address, and manager_id
- Manager: includes manager_id, name, salary, and showroom_id
- Sales: includes sales_id, car_id, customer_id, showroom_id, date, and price

## Relationships

The tables have the following relationships:

- Car has a one to many relationship with Sales
- Customer has a one to many relationship with Sales
- Showroom has a one to many relationship with Sales
- Showroom has a one to one relationship with Manager
- Manager has a one to one relationship with Showroom

## Features

The system provides the following features:

- CRUD operations to add, delete, and modify records from the tables
- An info page with general information about the project
- A sell operation that updates relevant tables in the backend when a car is sold

## Queries

The system supports the following queries:

- Most/Least expensive car models
- View managers above and below a certain salary threshold
- Most regular customer
- Car models with the highest sales based on the number of sales made

## ER Diagram

![Main_Page](https://user-images.githubusercontent.com/95089491/217521613-8fdc1db1-e3d3-4d54-ba08-261240c90bf7.jpg)
<p align="center">
  <strong>Main UI</strong>
</p>

## Schema Diagram

<!-- ![Main_Page](https://user-images.githubusercontent.com/95089491/217521613-8fdc1db1-e3d3-4d54-ba08-261240c90bf7.jpg)
<p align="center">
  <strong>Main UI</strong>
</p> -->

## Screenshots

<!-- ![Main_Page](https://user-images.githubusercontent.com/95089491/217521613-8fdc1db1-e3d3-4d54-ba08-261240c90bf7.jpg)
<p align="center">
  <strong>Main UI</strong>
</p>

![Main_Page](https://user-images.githubusercontent.com/95089491/217521613-8fdc1db1-e3d3-4d54-ba08-261240c90bf7.jpg)
<p align="center">
  <strong>Main UI</strong>
</p> -->


## Image URLS

![Cars_Table](https://user-images.githubusercontent.com/93508612/217592211-0678693a-87d6-462d-8e67-ba57021c25a6.png)
![Cars_With_Most_Sales](https://user-images.githubusercontent.com/93508612/217592224-fb27310c-6f87-44a5-8e64-9b5e791b4355.png)
![Create](https://user-images.githubusercontent.com/93508612/217592228-8c0a8c27-d8b5-437d-9706-494603658bec.png)
![Customer_table](https://user-images.githubusercontent.com/93508612/217592231-a6792184-f856-4fa9-8976-d86868b74664.png)
![ER_Diagram](https://user-images.githubusercontent.com/93508612/217592240-d69eff96-9e61-41c8-9622-96b674e9cf10.png)
![Info_Page](https://user-images.githubusercontent.com/93508612/217592247-7ed86a6c-772a-4e1b-8ac6-79c247b730de.jpg)
![Least_Expensive_Cars](https://user-images.githubusercontent.com/93508612/217592249-4527e750-f3d6-4b01-8e3a-1e5b899c9fe7.png)
![Login_Page](https://user-images.githubusercontent.com/93508612/217592255-cb885414-3277-42cf-afa6-83d12e3eef3a.png)
![Managers_table](https://user-images.githubusercontent.com/93508612/217592260-2bd72372-75f5-4644-9eca-f3991e35eb0f.png)
![Managers_with_salary_greater_than](https://user-images.githubusercontent.com/93508612/217592262-7bd6ce21-72e9-4a3b-8184-6a13e0ca0020.png)
![Most_Expensive_Cars](https://user-images.githubusercontent.com/93508612/217592269-840602f3-6ece-455d-a8b5-6c4a451892f7.png)
![Most_Regular_Customers](https://user-images.githubusercontent.com/93508612/217592274-238ab8b7-8de0-417c-a880-ff9f47f46ec5.png)
![Queries](https://user-images.githubusercontent.com/93508612/217592276-52d2adb6-ab5d-4cf1-9ec0-84df42ab8865.jpg)
![Queries2](https://user-images.githubusercontent.com/93508612/217592279-cbe1973a-ce15-4005-bd35-171fcea6f091.jpg)
![Sales_Table](https://user-images.githubusercontent.com/93508612/217592281-4968ef98-e4de-467f-9f1a-c623f27b2c28.png)
![Schema_Diagrma](https://user-images.githubusercontent.com/93508612/217592283-95d0ea53-bad8-4d77-a635-ad9e50ff4eb8.png)
![Sell](https://user-images.githubusercontent.com/93508612/217592286-b7afa843-655a-4cf6-9c04-f7a064684fb7.jpg)
![Showroom_Table](https://user-images.githubusercontent.com/93508612/217592290-0dac3abe-22f2-4700-a78f-a36309c6452c.png)
![Tables](https://user-images.githubusercontent.com/93508612/217592292-8bfd2677-a0fe-4772-97fa-32ee5a535f6f.png)







