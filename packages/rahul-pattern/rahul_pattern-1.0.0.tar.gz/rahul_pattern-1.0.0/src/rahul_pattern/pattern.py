def pattern_triangle(n):
    for i in range(n):
        for j in range(i+1):
            print("*", end=" ")
        print()
    for i in range(n):
        for j in range(n-i):
            print("*", end=" ")
        print()


def pattern_diamond(n):
    for i in range(n):
        for j in range(n-i):
            print(" ", end=" ")
        for j in range(i+1):
            print("*", end=" ")
        print()
    for i in range(n):
        for j in range(i+1):
            print(" ", end=" ")
        for j in range(n-i):
            print("*", end=" ")
        print()


def pattern_square(n):
    for i in range(n):
        for j in range(n):
            print("*", end=" ")
        print()


def pattern_rectangle(n, m):
    for i in range(n):
        for j in range(m):
            print("*", end=" ")
        print()
