from src.Validation import ReadIntInRange, ReadInt
from src.infra.database import AdminsDB, CoursesDB, StudentsDB, metaData, engine, SubjectsDB
from src.infra.student import Student
from src.infra.admin import Admin
from src.infra.security import PasswordHasher




students_db = StudentsDB()
courses_db = CoursesDB()
admins_db = AdminsDB()
subjects_db = SubjectsDB()

metaData.create_all(engine)

admins_db.ensure_default_admin()  # Ensure the default admin exists in the database

def CLS() -> None:
    print("\n" * 50)
    
def anyKeyToContinue()-> None:
    input("Press any key to continue...")

class MainScreen:
    
    ### ________student screen functions here _________ ###
    @staticmethod
    def _printOwnedCourses(student: Student) -> None:
        owned_courses = student.getOwnedCoursesFromCourses()
        if not owned_courses:
            print("No courses owned")
            return


        print(f"{'Course Name'.ljust(25)} {'Course Code'.ljust(15)} {'Credit Hours'.ljust(15)}")
        print("-" * 40)

        for course in owned_courses:
            print(f"{course['name'].ljust(25)} {course['code'].ljust(15)} {str(course['credit_hours']).ljust(15)}")


    @staticmethod
    def _printUnownedCourses(student: Student) -> None:
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
        
    @staticmethod
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
            MainScreen._printOwnedCourses(student)
            anyKeyToContinue()
            MainScreen._ShowStudentDetails(student)
        elif selection == 2:
            MainScreen._printUnownedCourses(student)
            course_code = input("Enter the course code to add: ")
            student.addCourse(course_code)
            anyKeyToContinue()
            MainScreen._ShowStudentDetails(student)
        elif selection == 3:
            MainScreen._printOwnedCourses(student)
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
        elif not PasswordHasher.verify_password(password, student_record["password"]):   
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
    ### ________admin screen functions here _________ ###
    

    @staticmethod
    def _adminValidationScreen() -> Admin | None:
        """Validate admin login credentials and return Admin object if valid"""
        print("Admin LogIn Screen .\n")
        user_name = input("Please enter your username: ")
        password = input("Please enter your password: ")
        admin_record = admins_db.select_by_user_name(user_name)
        if admin_record is None:   
            print("Admin not found")
            anyKeyToContinue()
            return None
        elif not PasswordHasher.verify_password(password, admin_record["password"]):    
            print("Incorrect password")
            anyKeyToContinue()
            
            return None
        else:
            admin = Admin(
                id=admin_record["id"],
                first_name=admin_record["first_name"],
                last_name=admin_record["last_name"],
                user_name=admin_record["user_name"],
                password=admin_record["password"],
                courses_db=courses_db,
                students_db=students_db,
                admins_db=admins_db
            )
            return admin
        

    
    @staticmethod
    def _goBackToTheprivilegeScreen()-> None:
        """Go back to the privilege screen"""
        MainScreen.ShowprivilegeScreen()
        
    @staticmethod
    def _goBackToTheAdminScreen(admin: Admin) -> None:
        """Go back to the admin screen"""
        welcome_message = f"Welcome {admin.getFullName()}!\n"
        print(welcome_message)
        MainScreen._showAdminChoices(admin)
    
    @staticmethod
    def _print_all_students(admin: Admin) -> None:
        """Print a list of students in a formatted table."""
        students = admin.view_all_students()
        print(f"{'ID'.ljust(5)} {'First Name'.ljust(15)} {'Last Name'.ljust(15)} {'Credit Hours'.ljust(15)}")
        print("-" * 50)
        for student in students:
            print(f"{str(student['id']).ljust(5)} {student['first_name'].ljust(15)} {student['last_name'].ljust(15)} {str(student['credit_hours']).ljust(15)}")
    @staticmethod        
    def _print_all_admins(admin: Admin) -> None:
        """Print a list of admins in a formatted table."""
        admins = admin.view_all_admins()
        print(f"{'ID'.ljust(5)} {'First Name'.ljust(15)} {'Last Name'.ljust(15)} {'Username'.ljust(20)}")
        print("-" * 60)
        for admin in admins:
            print(f"{str(admin['id']).ljust(5)} {admin['first_name'].ljust(15)} {admin['last_name'].ljust(15)} {admin['user_name'].ljust(20)}")
    
    @staticmethod        
    def _print_all_admins_exept_this(admin: Admin) -> None:
        """Print a list of admins in a formatted table."""
        admins = admin.view_all_admins()
        print(f"{'ID'.ljust(5)} {'First Name'.ljust(15)} {'Last Name'.ljust(15)} {'Username'.ljust(20)}")
        print("-" * 60)
        for adm in admins:
            if adm['id'] != admin.getId():
                print(f"{str(adm['id']).ljust(5)} {adm['first_name'].ljust(15)} {adm['last_name'].ljust(15)} {adm['user_name'].ljust(20)}")
    
    @staticmethod
    def _addNewAdmin(admin: Admin) -> None:
        """Add a new admin to the system."""
        new_admin = {
            "first_name": input("Enter first name: "),
            "last_name": input("Enter last name: "),
            "user_name": input("Enter username: "),
            "password": PasswordHasher.hash_password(input("Enter password: ")),
        }
        admin.add_new_admin(new_admin)
        print("Admin added successfully!")

    @staticmethod
    def _addNewStudent(admin: Admin) -> None:
        """Add a new student to the system."""
        new_student = {
            "first_name": input("Enter first name: "),
            "last_name": input("Enter last name: "),
            "password": PasswordHasher.hash_password(input("Enter password: ")),
            "credit_hours": 0
        }
        admin.add_new_student(new_student)
        print("Student added successfully!")
        
    @staticmethod
    def _deleteStudent(admin: Admin) -> None:
        """Delete a student from the system."""
        MainScreen._print_all_students(admin)
        student_id = ReadInt("Enter the ID of the student to delete: ")
        student = admin._students_db.select_by_id(student_id)
        if student is None:
            print("Student not found!")
            return
        admin.delete_student_by_id(student_id)
        print("Student deleted successfully!")
        
    @staticmethod
    
    def _deleteAdmin(admin: Admin) -> None:
        """Delete an admin from the system."""
        MainScreen._print_all_admins_exept_this(admin)
        num = admin._admins_db.number_of_records()
        if num == 1:
            print("Cannot delete the last admin.")
            return
        admin_id = ReadInt("Enter the ID of the admin to delete: ")
        admin.delete_admin_by_id(admin_id)
        admin = admin._admins_db.select_by_id(admin_id)
        if admin is not None:
            print("Admin not found!")
            return
        print("Admin deleted successfully!")
    @staticmethod
    def _addNewCourse(admin: Admin) -> None:
        """Add a new course to the system."""
        code = input("Enter course code: ")
        name = input("Enter course name: ")
        credit_hours = ReadInt("Enter credit hours: ")
        course = admin.get_course_by_code(code)
        if course:
            print("Course with this code already exists!")
            return
        admin.add_new_course(code, name, credit_hours)
        
        print("Course added successfully!")
        
    @staticmethod
    def _print_all_courses(admin: Admin) -> None:
        """Print a list of courses in a formatted table."""
        courses = admin.get_all_courses()
        print(f"{'Course Name'.ljust(25)} {'Course Code'.ljust(15)} {'Credit Hours'.ljust(15)}")
        print("-" * 50)
        for course in courses:
            print(f"{course['name'].ljust(25)} {course['code'].ljust(15)} {str(course['credit_hours']).ljust(15)}")
    
    @staticmethod
    def _deleteCourse(admin: Admin) -> None:
        """Delete a course from the system."""
        MainScreen._print_all_courses(admin)
        course_code = input("Enter the course code to delete: ")
        course = admin.get_course_by_code(course_code)
        if not course:
            print("Course not found!")
            return
        admin.delete_course_by_code(course_code)
        print("Course deleted successfully!")
           
    @staticmethod
    def _performAdminSelection(selection: int, admin: Admin) -> None:
        """Perform actions based on the selected admin option."""
        if selection == 1:
            MainScreen._print_all_students(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 2:
            MainScreen._print_all_admins(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 3:
            MainScreen._print_all_courses(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 4:
            MainScreen._addNewCourse(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 5:
            MainScreen._deleteCourse(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 6:
            MainScreen._addNewAdmin(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 7:
            MainScreen._addNewStudent(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 8:
            MainScreen._deleteStudent(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 9:
            MainScreen._deleteAdmin(admin)
            anyKeyToContinue()
            MainScreen._goBackToTheAdminScreen(admin)
        elif selection == 10:
            MainScreen._goBackToTheprivilegeScreen()
        
    @staticmethod
    def _showAdminChoices(admin: Admin) -> None:
        """Show admin choices in the admin screen"""
        print("1- View All Students")
        print("2- View All Admins")
        print("3- View All Courses")
        print("4- Add Course")
        print("5- Delete Course")
        print("6- Add New Admin")
        print("7- Add New Student")
        print("8- Delete Student")
        print("9- Delete Admin")
        print("10- Go Back\n")
        selection = MainScreen._choiceSelection("Please select an option: ", 1, 10)
        CLS()
        MainScreen._performAdminSelection(selection, admin)
    
    
    @staticmethod
    def _ShowAdminScreen()-> None:
        """Show the Admin Screen"""
        print("Welcome to the Admin Screen!\n")
        admin = MainScreen._adminValidationScreen()
        if admin is not None:
            # Add admin screen functionalities here
            print(f"Welcome {admin.getFullName()}!\n")
            MainScreen._showAdminChoices(admin)
        else:
            MainScreen._goBackToTheprivilegeScreen()
            


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
            
            
        ### ________mian screen functions here _________ ###        

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