from datetime import date
from uuid import uuid4


class User:
    def __init__(self, name, role, status):
        self.user_id = str(uuid4())
        self.name = name
        self.role = role.upper()
        self.status = status.upper()

        self.validate()

    def validate(self):
        if self.role not in ["ADMIN", "VIEWER", "ANALYST"]:
            raise ValueError("Role must be either ADMIN or VIEWER or ANALYST")
        if self.status not in ["ACTIVE", "INACTIVE"]:
            raise ValueError("Status must be either ACTIVE or INACTIVE")

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "role": self.role,
            "status": self.status,
        }


class FinancialRecord:
    def __init__(self, amount, record_type, category, dt):
        self.record_id = str(uuid4())
        self.amount = amount
        self.record_type = record_type.upper()
        self.category = category.upper()
        self.dt = dt

        self.validate()

    def validate(self):
        if not isinstance(self.amount, (int, float)):
            raise ValueError("Amount must be a number")
        if not isinstance(self.dt, date):
            raise ValueError("Invalid date format, expected YYYY-MM-DD")
        if self.record_type not in ["INCOME", "EXPENSE"]:
            raise ValueError("Record type must be either INCOME or EXPENSE")

    def to_dict(self):
        return {
            "id": self.record_id,
            "amount": self.amount,
            "type": self.record_type,
            "category": self.category,
            "date": self.dt,
        }


users = [
    User("Jack", "ADMIN", "ACTIVE"),
    User("James", "VIEWER", "INACTIVE"),
    User("Bob", "ANALYST", "ACTIVE"),
]


financial_records = [
    FinancialRecord(1000, "INCOME", "SALARY", date(2026, 4, 2)),
    FinancialRecord(200, "EXPENSE", "GROCERIES", date(2026, 4, 3)),
    FinancialRecord(150, "EXPENSE", "ENTERTAINMENT", date(2026, 4, 4)),
]
