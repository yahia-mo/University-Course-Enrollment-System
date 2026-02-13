from src.infra.courses import Courses
from src.infra.person import Person
from src.infra.security import PasswordHasher
from src.infra.database import AdminsDB, StudentsDB, CoursesDB

class Admin(Person, Courses):
    def __init__(self, id: int, first_name: str, last_name: str, user_name: str, password: str,
                 courses_db: CoursesDB, students_db: StudentsDB, admins_db: AdminsDB):
        super().__init__(first_name, last_name)
        self._id = id
        self._user_name = user_name
        self._password = password  # already hashed
        self._courses_db = courses_db
        self._students_db = students_db
        self._admins_db = admins_db

    def getId(self) -> int:
        return self._id

    def getUserName(self) -> str:
        return self._user_name

    def verify_password(self, password: str) -> bool:
        return PasswordHasher.verify(password, self._password)

    # Student management
    def add_new_student(self, student: dict):
        self._students_db.insert(student)


    def delete_student_by_id(self, student_id: int):
        self._students_db.delete_by_id(student_id)

    def view_all_students(self) -> list[dict]:
        return self._students_db.select_all()

    # Admin management
    def add_new_admin(self, admin: dict):
        self._admins_db.insert(admin)
        

    def delete_admin_by_id(self, admin_id: int):
        self._admins_db.delete_by_id(admin_id)

    def view_all_admins(self) -> list[dict]:
        return self._admins_db.select_all()
