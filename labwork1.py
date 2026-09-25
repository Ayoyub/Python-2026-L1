import math

#---------------LABWORK1.pdf-----------------#

#exo 1
radius = float(input("Enter circle radius: "))
area = radius*radius*3.14
print("Circle area = " , area )

#exo 2
celsius = int(input("\nEnter the temperature in Celsius: "))
farh=(celsius*(9/5))+32
print(f"{celsius} (C) = {farh} (F)")

#exo 3
print('\nPrime')
n = int(input("Enter a number (>2) : "))
prime=True
for i in range(2, n):
    if n % i ==0:
        prime=False
        break

if prime==False:
    print(f"{n} is NOT a prime number")
else:
    print(f"{n} is a prime number")

#exo 4
print('\nPerfect')
sum=0
n = int(input("Enter your number: "))
for i in range(1, n-1):
    if n % i ==0:
        sum+=i
if sum == n:
    print(f"{n} is a perfect number !")
else:
    print(f"{n} is NOT a perfect number")

#exo 5
user = str(input("\nWhats your favorite color ?\n"))
colors = ["red","Red","green","Green","blue","Blue","purple","Purple"]
if user in colors:
    for i in range(len(colors)):
        if colors[i]==user:
            index=i
    print(f"Your color is in my list at index {index}")
else:
    print("Sorry, I could not find your color.")

#exo 7
def remove_dollar_sign(s):
    """Removes any dollar sign from the string (s)"""
    string=list(s)
    clean_list=[i for i in string if i!="$"]
    result= "".join(clean_list)
    return result

print('\nTest of remove_dollar_sign function"')
stringtest=str(input("Enter your sentence containing $\n"))
print(remove_dollar_sign(stringtest))

#exo 8
def extract_even(l):
    """Extract only even numbers in given list l"""
    clean_list=[]
    for i in range(len(l)):
        if l[i]%2==0:
            clean_list.append(l[i])
        clean_list.sort()
    return clean_list

print("\nTest of function extract_even with list [1,4,5,-1,10].")
print(extract_even([1,4,5,-1,10]))

#exo 9
def factorial(n):
    '''Calculate the factorial of given number n'''
    fac = 1
    for i in range(n, 1, -1):
        fac= fac*i
    return fac
print("\nTest of factorial function")
fac_test=int(input("Enter your number: "))
print(factorial(fac_test))

#exo 10
def divisor(n):
    div=[1]
    """Returns all of divisors of the number n given in a list"""
    for i in range(n,1,-1):
        if n%i==0:
            div.append(i)
    return div
print("\nTesting of the function divisor")
n = int(input("Enter your number: "))
print(divisor(n))

#exo 11
def point_distance():
    """Returns the distance between two points (2D)"""
    x1=int(input("Enter the x coordinates of the first point: "))
    y1=int(input("Enter the y coordinates of the first point: "))
    x2=int(input("Enter the x coordinates of the second point: "))
    y2=int(input("Enter the y coordinates of the second point: "))
    dist=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist
print(point_distance())

#exo 12
def square_draw(m,n):
    '''Draws a square of asterisks, the sizes being m rows and n columns'''
    print("*" * n)
    for i in range(m-2):
        print("*" + " " * (n-2) + "*")
    print("*" * n)
square_draw(4, 5)
