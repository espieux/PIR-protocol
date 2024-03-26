from paillier import Paillier
from Crypto.PublicKey import DSA
from utils import sign_message
import pickle

class Client:
    def __init__(self, bits):
        self.phe = Paillier(bits)
        self.dsa_key = DSA.generate(2048)
        # Save the public key to a file
        with open("client_public_key.pem", "w") as f:
            f.write(self.dsa_key.publickey().export_key().decode('utf-8'))


    def request(self, db_size, index):
        v = [self.phe.encrypt(0) for _ in range(db_size)]
        v[index] = self.phe.encrypt(1)
        public_key = self.phe.public_key

        # Serialize data for signing
        data_to_sign = pickle.dumps((v, public_key))
        # Sign the request vector for authentication
        signature = sign_message(self.dsa_key, data_to_sign)

        return v, public_key, signature

    def decryptAnswer(self, encrypted_answer):
        return self.phe.decrypt(encrypted_answer)