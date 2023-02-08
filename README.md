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

## Schema Diagram

## Screenshots













