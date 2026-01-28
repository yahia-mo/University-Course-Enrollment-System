def ReadString(message: str) -> str:
<<<<<<< Updated upstream
    x: str = input(message)
    while not x.isalpha(): 
        x = input("Please enter a valid string (letters only): ")
    return x

def ReadInt(message: str) -> int:
    isValid: bool = False
    x_int: int = 0
    while not isValid:
        try:
            x_int = int(input(message))
        except ValueError:
            print("Please enter a valid integer.")
        else:
            isValid = True
    return x_int

def ReadFloat(message: str) -> float:
    isValid: bool = False
    x_float: float = 0
    while not isValid:
        try:
            x_float = float(input(message)) 
        except ValueError:
            print("Please enter a valid float number.")
        else:
            isValid = True
    return x_float

def ReadIntInRange(message: str, From: int, To: int) -> int:
    num: int = ReadInt(f"{message} ({From} - {To}): ")
    while num < From or num > To: 
        print("Input out of range.")
        num = ReadInt(f"{message} ({From} - {To}): ")
    return num

<<<<<<< HEAD
def ReadFloatInRange(message:str, From:float, To:float) -> float:
    num:float = ReadInt(message, f"({From}) : {To}")
    while num > To and num < From:
        print("Input Out Of Range .")
        num = ReadInt(message, f"({From}) : {To}")
    return num
=======
def ReadFloatInRange(message: str, From: float, To: float) -> float:
    num: float = ReadFloat(f"{message} ({From} - {To}): ")
    while num < From or num > To: 
        print("Input out of range.")
        num = ReadFloat(f"{message} ({From} - {To}): ")
=======
    """Reads a string input containing only letters."""
    x = input(message)
    while not x.isalpha():
        x = input("Please enter a valid string (letters only): ")
    return x


def ReadInt(message: str) -> int:
    """Reads an integer input."""
    while True:
        try:
            x_int = int(input(message))
            return x_int
        except ValueError:
            print("Please enter a valid integer.")


def ReadFloat(message: str) -> float:
    """Reads a float input."""
    while True:
        try:
            x_float = float(input(message))
            return x_float
        except ValueError:
            print("Please enter a valid number.")


def ReadIntInRange(message: str, From: int, To: int) -> int:
    """Reads an integer input and ensures it's within a specified range."""
    num = ReadInt(message + f" ({From}-{To}): ")
    while num < From or num > To:
        print("Input out of range.")
        num = ReadInt(message + f" ({From}-{To}): ")
    return num


def ReadFloatInRange(message: str, From: float, To: float) -> float:
    """Reads a float input and ensures it's within a specified range."""
    num = ReadFloat(message + f" ({From}-{To}): ")
    while num < From or num > To:
        print("Input out of range.")
        num = ReadFloat(message + f" ({From}-{To}): ")
>>>>>>> Stashed changes
    return num


>>>>>>> validation
