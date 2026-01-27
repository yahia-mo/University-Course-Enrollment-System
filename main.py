from src.infra.database import AdminsDB

database = AdminsDB()
database.insert({
    "first_name": "yehia",
    "last_name": "mohamed",
    "user_name": "yehia123",
    "password": 1234
})
database.delete_by_id(2)
x = database.select_by_username("yehia123")
print(x)