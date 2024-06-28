class Person:
    def __init__(self, id: int, name: str, age: int) -> None:
        self.id: int = id
        self.name: str = name
        self.age: int = age

    def __str__(self) -> str:
        return f"{self.id}:{self.name}:{self.age}"
    
    def isOldMajor(self) -> bool:
        return self.age >= 18
