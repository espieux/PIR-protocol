from utils import *
from Crypto.Util import number


class Paillier:
    def __init__(self, bits):
        self.keyGen(bits)

    def keyGen(self, bits):
        pass
        

    def encrypt(self, message: int):
        pass
    
    def decrypt(self, ciphertext: int):
        pass
        
    
phe = Paillier(1024)


m = "Trying to encrypt this message using Paillier"
c = phe.encrypt(string_to_int(m))
assert(int_to_string(phe.decrypt(c)) == m)