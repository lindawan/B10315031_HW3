import random

# generate big prime
def getPrime(n):
    number = 0
    while True:
        number = random.randrange(pow(2, n))
        if isPrime(number):
            break

    return number

# check whether the number is a prime
# using Miller-Rabin Test
def isPrime(n):
    if n<2 :
        return False
    elif n==2 or n==3:
        return True

    m = n-1
    k = 0
    while(m%2 == 0):
        m >>= 1
        k += 1

    a = random.randint(2, n-2)
    b = pow(a, m, n)
    if(b == 1 or b==n-1):
        return True

    for _ in range(k-1):
        b = pow(b, 2, n)
        if b==1:
            return False
        if b==n-1:
            return True

    return False

# Square and Multiply
def Square_Mul(x, e, n):
    H = [int(i) for i in bin(e)[2:]]
    y = x
    for i in H[1:]:
        y = (y**2) % n
        if i==1:
            y = y*x % n
    return y

#  Euclid's algorithm for determining the greatest common divisor
def gcd(a, b):
    while b!=0:
        a, b = b, a%b
    return a

# Euclid's extended algorithm for finding the multiplicative inverse of two numbers
def mul_inverse(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return  x0 if x0>0 else y0

# Chinese remainder theorem
def CRT(c, p, q, d, Dp, Dq, Qp):
    Mp = Square_Mul(c%p, Dp, p)
    Mq = Square_Mul(c%q, Dq, q)
    V = (Qp*(Mp-Mq)) % p
    return Mq + q*V


class RSA:
    def __init__(self):
        self.p = self.q = self.N = self.phiN = self.e = self.d = 0
        self.Dp = self.Dq = self.Qp = 0

    def setKeySize(self, size):
        self.keySize = size
        self.p = self.q = self.N = self.phiN = self.e = self.d = 0
        self.Dp = self.Dq = self.Qp = 0

    def getPubKey(self):
        return "N:" + str(hex(self.N)) + '\n\ne:' + str(hex(self.e))

    def getPrvKey(self):
        return "d:" + str(hex(self.d))
        
    def generate_key(self):
        # create p, q; p != q
        self.p = getPrime(self.keySize//2-1)
        self.q = getPrime(self.keySize//2)
        while self.p==self.q:
            self.q = getPrime(self.keySize//2)

        self.N = self.p * self.q
        self.phiN = (self.p-1) * (self.q-1)

        # e, phiN is relatively prime
        while True:
            self.e = random.randrange(1, self.phiN)
            if gcd(self.e, self.phiN)==1:
                break

        # ed = 1 (mod phiN)
        self.d = mul_inverse(self.e, self.phiN)

        # for CRT
        self.Dp = self.d % (self.p-1)
        self.Dq = self.d % (self.q-1)
        self.Qp = mul_inverse(self.q, self.p)

    def encrypt(self, m):
        # using Square and Multiply to speed up
        cipher = ''
        f = '{0:0%dx}' % (self.keySize//4)
        for char in m:
            cipher += f.format(Square_Mul(ord(char), self.e, self.N))
    
        return cipher

    def decrypt(self, c, method):
        plain = ''
        n = self.keySize//4
        
        if method == "Square and Multiply":
            # using Square and Multiply to speed up
            for i in range(0, len(c)-1, n):
                plain += chr(Square_Mul(int(c[i:i+n],16), self.d, self.N))
        elif method == "CRT":
            # using CRT to speed up
            for i in range(0, len(c)-1, n):
                plain += chr(CRT(int(c[i:i+n],16), self.p, self.q, self.d, self.Dp, self.Dq, self.Qp))
        return plain
        
