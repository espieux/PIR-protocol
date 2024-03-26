import random
from utils import verify_signature
import pickle

class Server:
    def __init__(self, size):
        self.database = [random.randint(1, 2**16) for _ in range(size)]
        self.size = size
        
    def answerRequest(self, request_vector, public_key, signature):
        # Verify the client's signature directly with the provided public key
        data_to_verify = pickle.dumps((request_vector, public_key))
        
        print("Verifying the signature...")
        if verify_signature("client_public_key.pem", data_to_verify, signature):
            # If verification succeeds, proceed with request processing
            n, g = public_key
            n_sq = n**2
            encrypted_sum = pow(g, 0, n_sq)

            for i in range(self.size):
                encrypted_value = pow(request_vector[i], self.database[i], n_sq)
                encrypted_sum = (encrypted_sum * encrypted_value) % n_sq
            return encrypted_sum
        else:
            # If verification fails, raise an error
            raise ValueError("Invalid signature")
