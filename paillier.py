from utils import *
from Crypto.Util import number

class Paillier:
    def __init__(self, bits):
        self.keyGen(bits)

    def keyGen(self, bits):
        p = q = n = 0
        while n.bit_length() != bits:
            # Generate two prime numbers p and q
            p = number.getPrime(bits // 2)
            q = number.getPrime(bits // 2)
            # Calculate the modulus n
            n = p * q
        # Calculate the generator g
        g = n + 1
        # Calculate the least common multiple of (p-1) and (q-1)
        lcm = (p-1) * (q-1) // number.GCD(p-1, q-1)
        # Calculate the modular inverse of lcm modulo n
        mu = pow(lcm, -1, n)
        # Store the generated values
        self.n = n
        self.n_sq = n * n
        self.g = g
        self.lmbda = lcm
        self.mu = mu
        
    def L(self, x):
        # Calculate the L function
        return (x - 1) // self.n

    def encrypt(self, message: int):
        if not (0 <= message < self.n):
            raise ValueError("Message must be in range 0 <= message < n")
        # Generate a random number r
        r = number.getRandomRange(1, self.n)
        # Ensure that r is coprime with n
        while number.GCD(r, self.n) != 1:
            r = number.getRandomRange(1, self.n)
        # Encrypt the message using the Paillier encryption algorithm
        c = pow(self.g, message, self.n_sq) * pow(r, self.n, self.n_sq) % self.n_sq
        return c

    def decrypt(self, ciphertext: int):
        # Decrypt the ciphertext using the Paillier decryption algorithm
        x = pow(ciphertext, self.lmbda, self.n_sq)
        m = (self.L(x) * self.mu) % self.n
        return m
        
    
def question1_test_encryption_decryption(phe, message):
    # Convert the string message to an integer for encryption
    c = phe.encrypt(string_to_int(message))
    # Decrypt the ciphertext and then convert the integer back to a string before verifying the result is correct
    assert int_to_string(phe.decrypt(c)) == message, "Decryption failed"

def question2_test_homomorphic_property(phe, m1, m2):
    # Encrypt two integers m1 and m2
    c1 = phe.encrypt(m1)
    c2 = phe.encrypt(m2)

    # Multiply the ciphertexts and decrypt the result
    c3 = (c1 * c2) % phe.n_sq
    m3 = phe.decrypt(c3)

    # The decrypted result should equal m1+m2
    assert m3 == m1 + m2, "Decryption failed"

def question3(phe, m1, m2):
    # Encrypt message m1 and directly compute encryption of m2 using g
    c1 = phe.encrypt(m1)
    gm2 = pow(phe.g, m2, phe.n_sq)

    # Multiply c1 by gm2 modulo n^2 and decrypt
    c4 = (c1 * gm2) % phe.n_sq
    m4 = phe.decrypt(c4)

    assert m4 == m1 + m2, "Decryption failed"

def question4(phe, m1, m2):
    # Encrypt message m1 and directly compute encryption of m2 using g
    c1 = phe.encrypt(m1)
    gm2 = pow(phe.g, m2, phe.n_sq)

    # This test is to understand the behavior, though not directly applicable for additive properties
    c5 = pow(c1, m2, phe.n_sq)
    # Decrypting c5 may not yield a meaningful result in the context of additive homomorphism

    m5 = phe.decrypt(c5)
    assert m5 == m1 * m2, "Decryption failed"


# Create an instance of the Paillier class with 1024-bit security
phe = Paillier(1024)

# Run the test cases
question1_test_encryption_decryption(phe, "Trying to encrypt this message using Paillier")
question2_test_homomorphic_property(phe, 123, 456)
question3(phe, 123, 456)
question4(phe, 123, 456)