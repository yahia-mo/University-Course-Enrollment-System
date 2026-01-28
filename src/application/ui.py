from src.Validation import  ReadIntInRange, ReadString, ReadInt
from src.infra.database import AdminsDB, CoursesDB, StudentsDB, metaData, engine, SubjectsDB
from src.infra.student import Student

students_db = StudentsDB()
courses_db = CoursesDB()
admins_db = AdminsDB()
subjects_db = SubjectsDB()
metaData.create_all(engine)

def CLS() -> None:
    print("\n" * 40)
def anyKeyToContinue()-> None:
    input("Press any key to continue...")

class MainScreen:
    
    @staticmethod
    def printOwnedCourses(student: Student) -> None:
        owned_courses = student.getOwnedCoursesFromCourses()
        if not owned_courses:
            print("No courses owned")
            return


        print(f"{'Course Name'.ljust(25)} {'Course Code'.ljust(15)} {'Credit Hours'.ljust(15)}")
        print("-" * 40)

        for course in owned_courses:
            print(f"{course['name'].ljust(25)} {course['code'].ljust(15)} {str(course['credit_hours']).ljust(15)}")


    @staticmethod
    def printUnownedCourses(student: Student) -> None:
        unowned_courses = student.getUnOwnedCourses()
        if not unowned_courses:
            print("No unowned courses available")
            return

        print(f"{'Course Name'.ljust(25)} {'Course Code'.ljust(15)} {'Credit Hours'.ljust(15)}")
        print("-" * 40)

        for course in unowned_courses:
            print(f"{course['name'].ljust(25)} {course['code'].ljust(15)} {str(course['credit_hours']).ljust(15)}")

    @staticmethod
    def _ShowStudentDetails(student: Student) -> None:
        """Display the details of a student."""
        CLS()
        print(f"welcome {student.getFirstName()}\n")
        print(f"Student ID: {student._id}")
        print(f"Full Name: {student.getFullName()}")
        print(f"Credit Hours: {student.getCreditHours()}\n")
        MainScreen._showUserChoices(student)
        

    def _showUserChoices(student: Student)-> None:
        """Show user choices in the student screen"""
        print("1- View Owned Courses")
        print("2- Add Course")
        print("3- Delete Course")
        print("4- Go Back\n")
        selection = MainScreen._choiceSelection("Please select an option: ", 1, 4)
        CLS()
        MainScreen._performStudentSelection(selection, student)

    @staticmethod
    def _performStudentSelection(selection: int, student: Student) -> None:
        """Perform actions based on the selected student option."""
        if selection == 1:
            MainScreen.printOwnedCourses(student)
            anyKeyToContinue()
            MainScreen._ShowStudentDetails(student)
        elif selection == 2:
            MainScreen.printUnownedCourses(student)
            course_code = input("Enter the course code to add: ")
            student.addCourse(course_code)
            anyKeyToContinue()
            MainScreen._ShowStudentDetails(student)
        elif selection == 3:
            MainScreen.printOwnedCourses(student)
            course_code = input("Enter the course code to delete: ")
            student.deleteCourse(course_code)
            anyKeyToContinue()
            MainScreen._ShowStudentDetails(student)
        elif selection == 4:
            MainScreen._goBackToTheprivilegeScreen()
            
    @staticmethod
    def _studentValidationScreen()-> Student | None:
        """Validate student login credentials and return Student object if valid"""
        print("LogIn Screen .\n")
        id = ReadInt("Please enter your ID: ")
        password = input("Please enter your password: ")
        student_record = students_db.select_by_id(id)
        if student_record is None:
            print("Student not found")
            anyKeyToContinue()
            return None
        elif student_record["password"] != password:
            print("Incorrect password")
            anyKeyToContinue()
            
            return None
        else:
            student = Student(
                first_name=student_record["first_name"],
                last_name=student_record["last_name"],
                password=student_record["password"],
                id=student_record["id"],
                courses_db=courses_db,
                subject_db=subjects_db,
                students_db=students_db
            )
            return student
        
    
    @staticmethod
    def _goBackToTheprivilegeScreen()-> None:
        """Go back to the privilege screen"""
        MainScreen.ShowprivilegeScreen()
        
        
    @staticmethod
    def _ShowAdminScreen()-> None:
        """Show the Admin Screen"""
        print("Welcome to the Admin Screen!\n")
        # Add admin screen functionalities here


    @staticmethod
    def _ShowStudentScreen()-> None:
        """Show the Student Screen"""
        print("Welcome to the Student Screen!\n")
        student = MainScreen._studentValidationScreen()
        if student is not None:
            # Add student screen functionalities here
            MainScreen._ShowStudentDetails(student)
            MainScreen._showUserChoices(student)
            
            
        else:
            MainScreen._goBackToTheprivilegeScreen()

    @staticmethod
    def _choiceSelection(message: str, From: int, To: int) -> int:
        """Get a choice selection from the user within a specified range."""
        selection = ReadIntInRange(message, From, To)
        return selection
    @staticmethod
    def _performPrivilegeSelection(selection: int):
        """Perform actions based on the selected privilege."""
        if selection == 1:
            MainScreen._ShowAdminScreen()
        elif selection == 2:
            MainScreen._ShowStudentScreen()
        elif selection == 3:
            print("Exiting the system .")
            exit()
        

    @staticmethod
    def ShowprivilegeScreen()-> None:
        """Display the privilege selection screen."""
        CLS()
        print("\n----------------")
        print("1- Admin Screen")
        print("2- Student Screen")
        print("3- Exit")
        print("----------------\n")
        selection = MainScreen._choiceSelection("Please select your privilege: ", 1, 3)
        CLS()
        MainScreen._performPrivilegeSelection(selection)  