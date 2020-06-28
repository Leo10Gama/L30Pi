def get_fib(n):
    if n < 0:
        return "Not a valid input"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return get_fib(n-1) + get_fib(n-2)