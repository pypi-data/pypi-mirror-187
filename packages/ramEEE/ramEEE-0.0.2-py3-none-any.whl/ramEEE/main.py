#To add Two numbers
def add_numbers(num1, num2):
    return num1 + num2
#To subtract Two numbers
def subtract_numbers(num1, num2):
    return num1 - num2
#To multiply Two numbers
def multiply_numbers(num1, num2):
    return num1 * num2
#To divide Two numbers
def divide_numbers(num1, num2):
    return num1 / num2
#To find factorial of a number
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)