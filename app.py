from flask import Flask, jsonify, request
from functools import wraps
from data import User, users, FinancialRecord, financial_records
from datetime import date


app = Flask(__name__)


def require_role(allowed_roles):
    """Decorator to check if the user has one of the allowed roles"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = request.headers.get("Role")
            if role not in allowed_roles:
                return {
                    "error": "Unauthorized You do not have permission to access this resource"
                }, 403
            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/api/users", methods=["GET"])
@require_role(["ADMIN"])
def get_users():
    """Get a list of users, optionally filtered by status"""
    filtered_users = users
    status = request.args.get("status")
    if status:
        filtered_users = [user for user in users if user.status == status.upper()]
    return jsonify([user.to_dict() for user in filtered_users]), 200


@app.route("/api/users", methods=["POST"])
@require_role(["ADMIN"])
def create_user():
    """Create a new user"""
    data = request.json
    if not data:
        return {"error": "Expected JSON data"}, 400
    name = data.get("name")
    role = data.get("role")
    status = data.get("status")

    if not name or not role or not status:
        return {
            "error": "Missing one or more required fields name, role, or status"
        }, 400

    try:
        new_user = User(name, role, status)
    except ValueError as e:
        return {"error": str(e)}, 400

    users.append(new_user)
    return jsonify(new_user.to_dict()), 201


@app.route("/api/users/<user_id>", methods=["PATCH"])
@require_role(["ADMIN"])
def update_user(user_id):
    """Update an existing user"""
    data = request.json
    if not data:
        return {"error": "Expected JSON data for update"}, 400

    name = data.get("name")
    role = data.get("role")
    status = data.get("status")

    if not name and not role and not status:
        return {
            "error": "At least one field (name, role, or status) must be provided for update"
        }, 400

    user = None
    for u in users:
        if u.user_id == user_id:
            user = u
            break
    if not user:
        return {"error": "User not found"}, 404

    try:
        if name:
            user.name = name
        if role:
            user.role = role.upper()
        if status:
            user.status = status.upper()
        user.validate()
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return {"error": str(e)}, 400


@app.route("/api/users/<user_id>", methods=["DELETE"])
@require_role(["ADMIN"])
def delete_user(user_id):
    """Delete a user"""
    user = None
    for u in users:
        if u.user_id == user_id:
            user = u
            break
    if not user:
        return {"error": "User not found"}, 404
    users.remove(user)
    return {"message": "User deleted"}, 200


@app.route("/api/records", methods=["GET"])
@require_role(["ADMIN", "VIEWER", "ANALYST"])
def get_records():
    """Get financial records"""
    return jsonify([record.to_dict() for record in financial_records]), 200


@app.route("/api/records", methods=["POST"])
@require_role(["ADMIN"])
def create_record():
    """Create a new financial record"""
    data = request.json
    if not data:
        return {"error": "Expected JSON data"}, 400
    amount = data.get("amount")
    record_type = data.get("type")
    category = data.get("category")
    dt = data.get("date")

    if not amount or not record_type or not category or not dt:
        return {
            "error": "Missing one or more required fields amount, type, category, or date"
        }, 400

    if record_type.upper() not in ["INCOME", "EXPENSE"]:
        return {"error": "Invalid record type, expected INCOME or EXPENSE"}, 400

    if dt:
        try:
            dt = date.fromisoformat(dt)
        except ValueError:
            return {"error": "Invalid date format, expected YYYY-MM-DD"}, 400

    try:
        new_record = FinancialRecord(amount, record_type, category, dt)
    except ValueError as e:
        return {"error": str(e)}, 400

    financial_records.append(new_record)
    return jsonify(new_record.to_dict()), 201


@app.route("/api/records/<record_id>", methods=["PATCH"])
@require_role(["ADMIN"])
def update_record(record_id):
    """Update an existing financial record"""
    data = request.json
    if not data:
        return {"error": "Expected JSON data for update"}, 400
    amount = data.get("amount")
    record_type = data.get("type")
    category = data.get("category")
    dt = data.get("date")

    if dt:
        try:
            dt = date.fromisoformat(dt)
        except ValueError:
            return {"error": "Invalid date format, expected YYYY-MM-DD"}, 400

    record = None
    for r in financial_records:
        if r.record_id == record_id:
            record = r
            break
    if not record:
        return {"error": "Record not found"}, 404

    try:
        if amount:
            record.amount = amount
        if record_type:
            record.record_type = record_type.upper()
        if category:
            record.category = category.upper()
        if dt:
            record.dt = dt
        record.validate()
    except ValueError as e:
        return {"error": str(e)}, 400

    return jsonify(record.to_dict()), 200


@app.route("/api/records/<record_id>", methods=["DELETE"])
@require_role(["ADMIN"])
def delete_record(record_id):
    """Delete a financial record"""
    record = None
    for r in financial_records:
        if r.record_id == record_id:
            record = r
            break
    if not record:
        return {"error": "Record not found"}, 404
    financial_records.remove(record)
    return {"message": "Record deleted"}, 200


@app.route("/api/records/insights", methods=["GET"])
@require_role(["ADMIN", "ANALYST"])
def get_insights():
    """Get financial insights"""
    total_income = sum(r.amount for r in financial_records if r.record_type == "INCOME")
    total_expense = sum(
        r.amount for r in financial_records if r.record_type == "EXPENSE"
    )
    net_balance = total_income - total_expense

    category = {}
    for r in financial_records:
        if r.category not in category:
            category[r.category] = 0
        if r.record_type == "INCOME":
            category[r.category] += r.amount
        elif r.record_type == "EXPENSE":
            category[r.category] -= r.amount

    recent_records = sorted(financial_records, key=lambda r: r.dt, reverse=True)[:5]
    return (
        jsonify(
            {
                "total_income": total_income,
                "total_expense": total_expense,
                "net_balance": net_balance,
                "category_data": category,
                "recent_records": [r.to_dict() for r in recent_records],
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
