from Crypto.Util.number import *
from sage.all import *
from secret import FLAG, x, y
import random

# D = {x∈ℕ | 0 ≤ x ≤ 1000}
# D = {y∈ℕ | 0 ≤ y ≤ 1000}

def enc(flag, polynomial_function):
    p = getStrongPrime(512)
    q = getStrongPrime(512)
    N = p * q
    e = 65537
    hint = p**3 - q**8 + polynomial_function(x=x)
    encrypted = pow(bytes_to_long(flag), e, N)
    print(f"N={N}")
    print(f"e={e}")
    print(f"hint={hint}")
    print(f"encrypted={encrypted}")


def generate_polynomial_function(seed):
    x = SR.var("x")
    random.seed(seed)
    grade = random.choice([2,3])
    a = random.randint(9999, 999999)
    b = random.randint(8888, 888888)
    c = random.randint(7777, 777777)

    if grade == 2:
        y_x = a*x**2+b*x+c
    if grade == 3:
        d = random.randint(6666, 666666)
        y_x = a*x**3+b*x**2+c*x+d

    print(a+b+c)
    return y_x


y_x = generate_polynomial_function(y)
enc(FLAG.encode(), y_x)