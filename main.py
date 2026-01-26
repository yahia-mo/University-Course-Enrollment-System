from src.infra.database import Database


database = Database()
database.InsertStatement({
    "first_name": "yehia",
    "last_name": "mohamed",
    "password": 1234,
    "credit_hours": 18
})

x = database.SelectById(1)
print(type(x))