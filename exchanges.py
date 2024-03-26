import time
import random
from client import Client
from server import Server
from Crypto.PublicKey import DSA

# Initialize client and server
client = Client(1024)
server = Server(100)  # Database size of 100

# Randomly select an index of interest
index_of_interest = random.randint(0, server.size - 1)

start_time = time.time()

# Client creates a request and signs it
request_vector, public_key, signature = client.request(100, index_of_interest)

# Server processes the request, verifies the signature, and returns the encrypted result
encrypted_answer = server.answerRequest(request_vector, public_key, signature)

# Client decrypts the received answer
decrypted_answer = client.decryptAnswer(encrypted_answer)

end_time = time.time() - start_time

# Verify that the decrypted answer matches the value in the server's database at the index of interest
assert decrypted_answer == server.database[index_of_interest], "The PIR protocol failed to retrieve the correct value."

print(f"The PIR protocol was successful.\nRetrieved value: {decrypted_answer}\nTime: {end_time}\n")
