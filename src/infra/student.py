from src.infra.person import Person
from src.infra.database import StudentsDB, SubjectsDB, CoursesDB

LIMITED_CREDIT_HOURS = 18

class Student(Person):
    def __init__(self, id: int, first_name: str, last_name: str, password: str,
                 courses_db: CoursesDB, subject_db: SubjectsDB, students_db: StudentsDB):
        super().__init__(first_name, last_name)
        self._id = id
        self._password = password
        self._courses_db = courses_db
        self._subject_db = subject_db
        self._students_db = students_db
        self._creditHours = subject_db.getCreditHours_by_student_id(self._id)


    def getCreditHours(self) -> int:
        return self._creditHours

    def getOwnedCoursesFromSubjects(self) -> list[dict]:
        return self._subject_db.select_by_student_id(self._id)

    def getOwnedCoursesFromCourses(self) -> list[dict]:
        owned_subjects = self.getOwnedCoursesFromSubjects()
        owned_names = {s["name"] for s in owned_subjects}
        return [c for c in self._courses_db.select_all() if c["name"] in owned_names]

    def getUnOwnedCourses(self) -> list[dict]:
        owned_names = {c["name"] for c in self.getOwnedCoursesFromSubjects()}
        return [c for c in self._courses_db.select_all() if c["name"] not in owned_names]

    def addCourse(self, course_code: str):
        course = self._courses_db.select_by_code(course_code)
        if not course:
            print("Course not found")
            return
        if course["credit_hours"] + self._creditHours > LIMITED_CREDIT_HOURS:
            print("Credit hours exceed limit")
            return
        owned_names = {c["name"] for c in self.getOwnedCoursesFromSubjects()}
        if course["name"] in owned_names:
            print("Course already owned")
            return
        self._subject_db.insert({
            "name": course["name"],
            "student_id": self._id,
            "credit_hours": course["credit_hours"]
        })
        self._creditHours += course["credit_hours"]
        self._students_db.update_by_id(self._id, {"credit_hours": self._creditHours})
        print("Course added successfully")

    def deleteCourse(self, course_code: str):
        course_name = None
        course = self._courses_db.select_by_code(course_code)
        if course:
            course_name = course["name"]
        if not course_name:
            print("Course not found")
            return
        for c in self.getOwnedCoursesFromSubjects():
            if c["name"] == course_name:
                self._subject_db.delete_by_id(c["id"])
                self._creditHours -= c["credit_hours"]
                self._students_db.update_by_id(self._id, {"credit_hours": self._creditHours})
                print("Course deleted successfully")
                return
        print("Course not owned")
