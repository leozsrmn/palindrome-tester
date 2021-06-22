from ctypes import *
import sys
import colorama
import json
import math


## SRC : https://stackoverflow.com/questions/2489435/check-if-a-number-is-a-perfect-square
## perfectsqure func are not my code

def perfectsquare(n):
    ## Trivial checks
    if type(n) != int:  ## integer
        return False
    if n < 0:      ## positivity
        return False
    if n == 0:      ## 0 pass
        return True

    ## Reduction by powers of 4 with bit-logic
    while n&3 == 0:
        n=n>>2

    ## Simple bit-logic test. All perfect squares, in binary,
    ## end in 001, when powers of 4 are factored out.
    if n&7 != 1:
        return False

    if n==1:
        return True  ## is power of 4, or even power of 2


    ## Simple modulo equivalency test
    c = n%10
    if c in {3, 7}:
        return False  ## Not 1,4,5,6,9 in mod 10
    if n % 7 in {3, 5, 6}:
        return False  ## Not 1,2,4 mod 7
    if n % 9 in {2,3,5,6,8}:
        return False
    if n % 13 in {2,5,6,7,8,11}:
        return False

    ## Other patterns
    if c == 5:  ## if it ends in a 5
        if (n//10)%10 != 2:
            return False    ## then it must end in 25
        if (n//100)%10 not in {0,2,6}:
            return False    ## and in 025, 225, or 625
        if (n//100)%10 == 6:
            if (n//1000)%10 not in {0,5}:
                return False    ## that is, 0625 or 5625
    else:
        if (n//10)%4 != 0:
            return False    ## (4k)*10 + (1,9)


    ## Babylonian Algorithm. Finding the integer square root.
    ## Root extraction.
    s = (len(str(n))-1) // 2
    x = (10**s) * 4

    A = {x, n}
    while x * x != n:
        x = (x + (n // x)) >> 1
        if x in A:
            return False
        A.add(x)
    return True


def get_function(path):
    my_function = CDLL(path)
    return my_function


def square_root(nb):
    if nb < 0:
        return -1
    if nb == 0:
        return 0
    if nb > 2147483647 or nb < -2147483646:
        return 0
    if not perfectsquare(nb):
        return -1
    return math.sqrt(nb)


def ft_squareroot(requirement, testid, numbers):
    test_failed = 0
    test_passed = 0
    print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}---" + testid + f"---{colorama.Style.RESET_ALL}")
    for i in numbers:
        got_result = requirement.my_squareroot_synthesis(i)
        good_result = square_root(i)
        if good_result != got_result:
            print("failed (" + str(i) + "):\nGot: " + str(got_result) + "\nBut expected: " + str(int(good_result)))
            test_failed += 1
        else:
            test_passed += 1
    if test_failed == 0:
        print(f"{colorama.Fore.GREEN}Passed (" + str(test_passed) + f" tests).{colorama.Style.RESET_ALL}")


def factorial(nb):
    if nb >= 13 or nb < 0:
        return 0
    return math.factorial(nb)


def ft_factorial(requirement, testid, numbers):
    test_failed = 0
    test_passed = 0
    print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}---" + testid + f"---{colorama.Style.RESET_ALL}")
    print("args: " + str(numbers))
    for i in numbers:
        got_result = requirement.my_factrec_synthesis(i)
        good_result = factorial(i)
        if good_result != got_result:
            print("failed (" + str(i) + "):\nGot: " + str(got_result) + "\nBut expected: " + str(int(good_result)))
            test_failed += 1
        else:
            test_passed += 1
    if test_failed == 0:
        print(f"{colorama.Fore.GREEN}Passed (" + str(test_passed) + f" tests).{colorama.Style.RESET_ALL}")


def run_tests(tests, requirement):
    for key, test in tests.items():
        if test['ft'] == "squareroot":
            print("ft/squareroot")
            ft_squareroot(requirement, test['name'], test['numbers'])
        if test['ft'] == "factorial":
            print("ft/factorial")
            ft_factorial(requirement, test['name'], test['numbers'])
        print("")


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("miss path")
        exit(0)
    functions = get_function("./requirement.so")
    file = open(sys.argv[1], "r")
    raw = json.load(file)
    run_tests(raw, functions)