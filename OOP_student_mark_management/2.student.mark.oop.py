class Student:
    __name = "Null"
    __id = 0
    __dob = "Null"

    def __init__(self, a ,b ,c):
        self.__name = a
        self.__id = b
        self.__dob = c

    def getName(self):
        return self.__name

    def getId(self):
        return self.__id

    def getDob(self):
        return self.__dob

ayoub = Student("ayoub", 100, "22/06/2007")

print(ayoub.getName())
print(ayoub.getId())
print(ayoub.getDob())

class Course:
    __name = "Null"
    __id = 0
    __credits = 0

    def __init__(a,b,c):
        __name = a
        __id = b
        __credits=c

    def getName(self):
        return self.__name