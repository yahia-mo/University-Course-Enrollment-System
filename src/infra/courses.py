from src.infra.database import CoursesDB

class Courses():
    def __init__(self, Courses_DB: CoursesDB):
        self._courses_db = Courses_DB


    def add_course(self, code: str, name: str, credit_hours: int) -> None:
        course_data = {
            "code": code,
            "name": name,
            "credit_hours": credit_hours
        }
        self._courses_db.insert(course_data)

    def get_all_courses(self) -> list[dict]:
        return self._courses_db.select_all()
    
    def get_course_by_code(self, code: str) -> dict | None:
        return self._courses_db.select_by_code(code)
    
    
    
    
    
    
    
    
  