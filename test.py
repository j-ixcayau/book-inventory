from person import Person


print("Hola Mundo")

p1 = Person(1,"Jonathan", 16)

print(p1)
print(f"Es mayor de edad: {"Si" if p1.isOldMajor() else "No"}")