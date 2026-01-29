from person import Person
from Validation import ReadString, ReadInt
from student import Student
from security import PasswordHasher
from infra.database import AdminsDB, StudentsDB

class Admin(Person):
    def __init__(self, first_name: str, last_name: str, user_name: str, password: str):
        super().__init__(first_name, last_name)
        self._user_name: str = user_name
        self._password: str = PasswordHasher.hash_password(password)

    def setUserName(self, user_name: str) -> None:
        self._user_name = user_name
         
    def setPassword(self, password: str) -> None:
        self._password = password
        
    def getUserName(self) -> str:
        return self._user_name

    def verify_password(self, password: str) -> bool:
        return PasswordHasher.verify(password, self._password_hash)

# todo:(abdo) add function that add new student and return student object

    
#todo:(abdo) add function that add new admin and return admin object

#todo:(abdo) add function that take a student object and save it to database

#todo:(abdo) add function that take an admin object and save it to database

#todo:(abdo) add function that view all admins return list of admins dict.

# todo:(abdo) add function that view all students return list of students dict.