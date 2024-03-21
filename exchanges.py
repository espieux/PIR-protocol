from client import Client
from server import Server

# Initialize client and server
client = Client(1024)
server = Server(100)  # Database size of 100

# Client makes a request for a specific element, say index 50
index_of_interest = 50
request_vector, public_key = client.request(100, index_of_interest)

# Server processes the request and returns the encrypted result
encrypted_answer = server.answerRequest(request_vector, public_key)

# Client decrypts the received answer
decrypted_answer = client.decryptAnswer(encrypted_answer)

# Verify that the decrypted answer matches the value in the server's database at the index of interest
assert decrypted_answer == server.database[index_of_interest], "\n\nThe PIR protocol failed to retrieve the correct value.\n\n"

print(f"\n\nThe PIR protocol was successful.\nRetrieved value: {decrypted_answer}\n\n")