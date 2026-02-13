from src.infra.database import CoursesDB

class Courses:
    def __init__(self, courses_db: CoursesDB):
        self._courses_db = courses_db

    def add_new_course(self, code: str, name: str, credit_hours: int):
        self._courses_db.insert({"code": code, "name": name, "credit_hours": credit_hours})

    def get_all_courses(self) -> list[dict]:
        return self._courses_db.select_all()

    def get_course_by_code(self, code: str) -> dict | None:
        return self._courses_db.select_by_code(code)

    def delete_course_by_code(self, code: str):
        course = self._courses_db.select_by_code(code)
        if course:
            self._courses_db.delete_by_id(course["id"])
