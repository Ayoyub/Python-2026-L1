from domains.student import Student

def input_student_info():
    id = input("\tStudent's ID is: ")
    name = input("\tYour name: ")
    dob = input("\tDate of birth: ")
    return Student(id, name, dob)

