import infra.person as person

class Student (person):
    def __init__(self, first_name:str, last_name:str, password:int):
        super().__init__(first_name, last_name)
        self._creditHours:int = 18
        self._password:int = password