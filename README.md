# Finance Data Processing and Access Control Backend

## Overview

This project is a simple backend system for a finance dashboard that manages users, financial records, and summary insights with role-based access control.

This project focuses on building and showcasing core backend concepts such as:

- API design
- Data modeling
- Access control
- Input validation
- Business logic implementation

Custom classes are used instead of an ORM to keep the project lightweight

## Tech Stack

- Language: Python
- Framework: Flask
- Data Storage: In-memory (Python lists)

## Note: No database is used. Data is stored in memory for simplicity and to focus on API design.

## Tradeoffs & Limitations

- Data is stored in memory, so it resets on server restart
- No authentication system (role is passed via headers)
- Not optimized for production use

## System Design

The backend is structured into:

- API routes (Flask)
- Data models (`User`, `FinancialRecord`)
- In-memory storage (`users`, `financial_records`)
- Access control decorator (`require_role`)

## User and Role Management

### Roles

- ADMIN  
  Full access (create/update/delete users and records)
- ANALYST  
  Can view records and access insights
- VIEWER  
  Can only view records

### Features

- Create users
- Update users
- Delete users
- Filter users by status (ACTIVE / INACTIVE)

## Financial Records Management

Each record contains:

- amount
- type (INCOME / EXPENSE)
- category
- date

### Supported Operations

- Create records
- View records
- Update records
- Delete records

## Dashboard Insights

Provides:

- Total income
- Total expense
- Net balance
- Category-wise totals
- Recent transactions

## Access Control

Access control is implemented using a custom decorator:

@require_role([...])

## API Endpoints

## API Endpoints

### Users

- GET `/api/users`
- POST `/api/users`
- PATCH `/api/users/<id>`
- DELETE `/api/users/<id>`

Optional:

- Filter by status: `/api/users?status=ACTIVE`

### Records

- GET `/api/records`
- POST `/api/records`
- PATCH `/api/records/<id>`
- DELETE `/api/records/<id>`

### Dashboard Insights

- GET `/api/records/insights`

### Sample Requests

Create User

POST /api/users  
Headers: Role: ADMIN

Body:
{
"name": "Alice",
"role": "ANALYST",
"status": "ACTIVE"
}

Create Record

POST /api/records  
Headers: Role: ADMIN

Body:
{
"amount": 500,
"type": "INCOME",
"category": "FREELANCE",
"date": "2026-04-02"
}

## Running the Project

1. Create virtual environment and activate it
   python -m venv venv
   source venv/bin/activate

2. Install dependencies
   pip install -r requirements.txt

3. Run the server
   python app.py
   Server will be available at http://127.0.0.1:5000 and we can use tools like curl or postman to start making requests
