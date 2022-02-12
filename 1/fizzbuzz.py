

def exchange_for_fizz_buzz(n):
    try:
        n = round(int(n))
    except ValueError:
        raise ValueError("Please insert a valid number  ")

    if n > 100 or n < 1:
        raise ValueError("needs to be in the range between of 1 to 100 ")


    lst = []
    
    for i in range(1, n + 1 ):
        if i % 3 == 0 and i % 5 == 0:
            lst.append('FizzBuzz')
        elif i % 3 == 0:
            lst.append('Fizz')
        elif i % 5 == 0 :
            lst.append("Buzz")
        else:
            lst.append(str(i))
    return lst



if __name__ == '__main__':

    n = input("Please insert a number  ")
    output = exchange_for_fizz_buzz(n)
    print(output)



