from src.infra.person import Person
from src.infra.database import SubjectsDB, CoursesDB, StudentsDB



LIMITED_CREDIT_HOURS = 18
class Student (Person):
    def __init__(self,id: int ,first_name:str, last_name:str, password:str, courses_db:CoursesDB, subject_db:SubjectsDB, students_db: StudentsDB ):
        super().__init__(first_name, last_name)
        self._password: str= password
        self._courses_db = courses_db
        self._subject_db = subject_db
        self._students_db = students_db
        self._id: int = id
        self._creditHours:int = subject_db.getCreditHours_by_student_id(self._id)

    def setCreditHours(self, creditHours:int) -> None:
        self._creditHours = creditHours
    
    def setPassword(self, password:str) -> None:
        self._password = password
        
    def getCreditHours(self) -> int:
        return self._creditHours

    def getPassword(self) -> str:
        return self._password

    def getOwnedCoursesFromSubjects(self) -> list[dict]:
        return self._subject_db.select_by_student_id(self._id)
    
    def getOwnedCoursesFromCourses(self) -> list[dict]:
        owned_subjects = self._subject_db.select_by_student_id(self._id)
        owned_course_names = {subject["name"] for subject in owned_subjects}

        all_courses = self._courses_db.select_all()
        owned_courses = [
            course for course in all_courses
            if course["name"] in owned_course_names
        ]

        return owned_courses
    def getUnOwnedCourses(self) -> list[dict]:
        owned_courses = self.getOwnedCoursesFromSubjects()
        owned_course_names = {course["name"] for course in owned_courses}

        all_courses = self._courses_db.select_all()
        unowned_courses = [
            course for course in all_courses
            if course["name"] not in owned_course_names
        ]

        return unowned_courses
    
    def addCourse(self, course_code: str) -> None:
        Course = self._courses_db.select_by_code(course_code)
        owned_courses = self.getOwnedCoursesFromSubjects()

        if Course is None:
            print("Course not found")
            return

        if Course["credit_hours"] + self._creditHours > LIMITED_CREDIT_HOURS:
            print("Credit hours exceed the limit")
            return

        for owned_course in owned_courses:
            if owned_course["name"] == Course["name"]:
                print("Course already owned")
                return

        subject_data = {
            "name": Course["name"],
            "student_id": self._id,
            "credit_hours": Course["credit_hours"]
        }

        self._subject_db.insert(subject_data)
        self._creditHours += Course["credit_hours"]
        self._students_db.update_by_id(self._id, {"credit_hours": self._creditHours})
        print("Course added successfully")


                
    def deleteCourse(self, course_code: str) -> None:
        owned_courses = self.getOwnedCoursesFromSubjects()
        course_name = self.getCourseNameByCode(course_code)
        if course_name is None:
            print("Course not found")
            return
        for owned_course in owned_courses:
            if owned_course["name"] == course_name:
                self._subject_db.delete_by_id(owned_course["id"])
                self._creditHours -= owned_course["credit_hours"]
                self._students_db.update_by_id(self._id, {"credit_hours": self._creditHours})
                print("Course deleted successfully")
                return
        print("Course not owned")
        
    def getCourseNameByCode(self, course_code: str) -> str | None:
        course = self._courses_db.select_by_code(course_code)
        if course:
            return course["name"]
        return None

        
            
        
        
    
    
        
        
    