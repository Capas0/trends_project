def fib(n):
    a, b = 0, 1
    for _ in range(n + 1):
        yield a
        a, b = b, a + b


print(list(fib(10)))
