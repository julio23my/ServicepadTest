def fibonacci_search_recursive(n):
    try:
        n = round(int(n))
    except ValueError:
        raise ValueError("Please insert a valid number  ")

    if n<= 0 or n >= 40 :
        raise ValueError("needs to be in the range between of 1 to 40 ")

    elif n == 1:
        return 0

    elif n == 2:
        return 1

    else:
        return fibonacci_search_recursive(n-1)+fibonacci_search_recursive(n-2)
 
 
if __name__ == '__main__':

    n = input("Please insert a number to find in fibonacci  ")
    output = fibonacci_search_recursive(n)
    print(output)
