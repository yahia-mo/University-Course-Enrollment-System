from src.infra.person import Person
from src.infra.database import SubjectsDB, CoursesDB



LIMITED_CREDIT_HOURS = 18
class Student (Person):
    def __init__(self, first_name:str, last_name:str, password:str, courses_db:CoursesDB, subject_db:SubjectsDB ):
        super().__init__(first_name, last_name)
        self._creditHours:int = 0
        self._password: str= password
        self._courses_db = courses_db
        self._subject_db = subject_db

    def setCreditHours(self, creditHours:int) -> None:
        self._creditHours = creditHours
    
    def setPassword(self, password:str) -> None:
        self._password = password
        
    def getCreditHours(self) -> int:
        return self._creditHours

    def getPassword(self) -> str:
        return self._password

    def getOwnedCourses(self) -> list[dict]:
        result = self._subject_db.select_by_student_id(self._id)
        return result
    
    def addCourse(self, course_id: str) -> None:
        Course = self._courses_db.get_course_by_code(course_id)
        owned_courses = self.getOwnedCourses()
        if Course is None:
            print("Course not found")
            return
        elif Course["credit_hours"] + self._creditHours > LIMITED_CREDIT_HOURS:
            print("Credit hours exceed the limit")
            return
        else:
            for owned_course in owned_courses:
                if owned_course["course_id"] == Course["id"]:
                    print("Course already owned")
                    return
        
        subject_data = {
            "name": Course["name"],
            "course_id": course_id,
            "student_id": self._id
        }
        self._subject_db.insert(subject_data)
        self._creditHours += Course["credit_hours"]
        print("Course added successfully")
        
        
    def printOwnedCourses(self) -> None:
        owned_courses = self.getOwnedCourses()
        if not owned_courses:
            print("No courses owned")
            return
        print("Owned Courses:")
        for course in owned_courses:
            course_info = self._courses_db.get_course_by_code(course["course_id"])
            if course_info:
                print(f"- {course_info['name']} (Code: {course_info['code']}, Credit Hours: {course_info['credit_hours']})")
                
    def deleteCourse(self, course_id: str) -> None:
        owned_courses = self.getOwnedCourses()
        for owned_course in owned_courses:
            if owned_course["course_id"] == course_id:
                self._subject_db.delete_by_id(owned_course["id"])
                course_info = self._courses_db.get_course_by_code(course_id)
                if course_info:
                    self._creditHours -= course_info["credit_hours"]
                print("Course deleted successfully")
                return
        print("Course not found in owned courses")
            
        
            
        
        
    
    
        
        
    