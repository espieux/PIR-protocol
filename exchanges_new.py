import time
from client_new import Client
from server_new import Server, random

# Specify dimensions of the 2D database
db_rows = 10
db_columns = 10

# Initialize client and server
client = Client(1024)
server = Server(db_rows, db_columns)

# Randomly select row and column indices of interest
row_index_of_interest = random.randint(0, db_rows - 1)
col_index_of_interest = random.randint(0, db_columns - 1)

# Client generates a request for the specific element
start_time = time.time()
request_vectors, public_key = client.request(db_rows, db_columns, row_index_of_interest, col_index_of_interest)

# Server processes the request and returns the encrypted results
encrypted_answers = server.answerRequest(request_vectors, public_key)

# Client decrypts the received answer for the specific column
decrypted_answer = client.decryptAnswer(encrypted_answers[col_index_of_interest])

end_time = time.time() - start_time

# Verify that the decrypted answer matches the value in the server's database at the specified row and column
assert decrypted_answer == server.database[row_index_of_interest][col_index_of_interest], "PIR protocol failed to retrieve the correct value."

print(f"PIR protocol was successful.\nRetrieved value: {decrypted_answer}\nAt position [N,M] = [{row_index_of_interest},{col_index_of_interest}]\nTime taken: {end_time} seconds")