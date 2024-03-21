import random  
class Server:
    def __init__(self, size):
        self.database = [random.randint(1, 2**16) for _ in range(size)]
        self.size = size
    
    def answerRequest(self, request_vector, public_key):
        # Prepare the sum (initialize to 0 encrypted with the client's public key)
        n, g = public_key
        n_sq = n**2
        encrypted_sum = pow(g, 0, n_sq)  # This is Enc(0) using the client's public key

        # Homomorphically sum up the requested database value
        for i in range(self.size):
            # Use the propriety seen in question 4 to create a cyphertext = to m1*m2
            encrypted_value=pow(request_vector[i],self.database[i],n_sq)
            # Use the additive propriety to sum the cyphertexts
            encrypted_sum = (encrypted_sum * encrypted_value) % n_sq
        return encrypted_sum