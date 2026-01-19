def ReadString(message:str) -> str:
    x:str = input(message)
    while(not x.isalpha):
        x = input("Please Enter a Valid Type.")
    return x

def ReadInt(message:str) -> int:
    isValid:bool = False
    x_int:int = 0
    while not isValid:
        try:
            int(input(message))
        except TypeError :
            x = input("Please Enter a Valid Type.")
        else:
            isValid = True
    return x_int
            
def ReadFloat(message:str) -> float:
    x:str = input(message)
    isValid:bool = False
    x_float:float = 0
    while isValid:
        try:
            x_float = int(x)
        except TypeError :
            x = input("Please Enter a Valid Type.")
        else:
            isValid = True
    return x_float

def ReadIntInRange(message:str, From:int, To:int) -> int:
    num:int = ReadInt(message, f"({From}) : {To}")
    while num > To and num < From:
        print("Input Out Of Range .")
        num = ReadInt(message, f"({From}) : {To}")
    return num

def ReadFloatInRange(message:str, From:float, To:float) -> float:
    num:float = ReadInt(message, f"({From}) : {To}")
    while num > To and num < From:
        print("Input Out Of Range .")
        num = ReadInt(message, f"({From}) : {To}")
    return num