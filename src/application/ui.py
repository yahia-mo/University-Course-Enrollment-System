from src.Validation import  ReadIntInRange
from src.infra.database import AdminsDB, CoursesDB, StudentsDB, metaData, engine, SubjectsDB
from src.infra.student import Student

students_db = StudentsDB()
courses_db = CoursesDB()
admins_db = AdminsDB()
subjects_db = SubjectsDB()
metaData.create_all(engine)

class MainScreen:
    
    
    @staticmethod
    def _ShowAdminScreen():
        print("Welcome to the Admin Screen!")
        # Add admin screen functionalities here

    @staticmethod
    def _ShowStudentScreen():
        print("Welcome to the Student Screen!")
        # Add student screen functionalities here
    
    @staticmethod
    def _choiceSelection(message: str, From: int, To: int) -> int:
        selection = ReadIntInRange(message, From, To)
        return selection
    @staticmethod
    def _performPrivilegeSelection(selection: int):
        if selection == 1:
            MainScreen._ShowAdminScreen()
        elif selection == 2:
            MainScreen._ShowStudentScreen()

    @staticmethod
    def ShowprivilegeScreen():
        print("1- Admin Screen")
        print("2- Student Screen")
        selection = MainScreen._choiceSelection("Please select your privilege: ", 1, 2)
        MainScreen._performPrivilegeSelection(selection)  