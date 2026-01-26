class Person:
    def __init__(self,first_name:str,last_name:str):
        self._id:int
        self._first_name:str = first_name
        self._last_name:str = last_name
        self._full_name:str = self._first_name + " " + self._last_name
        
def setFirstName(self, FirstName) -> None:
    self._first_name = FirstName

def setLastName(self, LastName) -> None:
    self._last_name = LastName

        
def GetFirstName(self, FirstName) -> str:
    return self._first_name

def GetLastName(self, LastName) -> str: 
    return self._last_name 
