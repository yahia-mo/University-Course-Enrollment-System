from person import Person

class Admin(Person):
    def __init__(self, first_name: str, last_name: str, user_name: str, password: int):
        super().__init__(first_name, last_name)
        self._user_name: str = user_name
        self._password: int = password

    def setUserName(self, user_name: str) -> None:
        self._user_name = user_name
         
    def setPassword(self, password: str) -> None:
        self._password = password
        
    def getUserName(self) -> str:
        return self._user_name

    def getPassword(self) -> str:
        return self._password
    
x = Admin("Yahya", "Mohamed", "yahya123", 1234)
y = x.getUserName()
print(y)