from paillier import Paillier

class Client:
    def __init__(self, bits):
        self.phe = Paillier(bits)  # Initialize Paillier cryptosystem with the given bit length
    
    def request(self, db_size, index):
        # Generate a vector of encrypted zeros with an encrypted one at the specified index
        v = [self.phe.encrypt(0) for _ in range(db_size)]
        v[index] = self.phe.encrypt(1)  # Encrypt 1 at the specified index
        return v, self.phe.public_key  # Return the vector and public key as the request

    def decryptAnswer(self, encrypted_answer):
        # Decrypt the encrypted answer from the server using the client's private key
        return self.phe.decrypt(encrypted_answer)