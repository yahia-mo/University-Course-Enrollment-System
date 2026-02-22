def ReadString(message: str, impty_message: str) -> str:
    """Reads a string input containing only letters."""
    x = input(message).strip()
    while x == "" :
        print(impty_message)
        x = input(message).strip()
        
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
    return num


