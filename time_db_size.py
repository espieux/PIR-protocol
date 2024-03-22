import time
import matplotlib.pyplot as plt
import random
from client import Client
from server import Server

# Define the range of database sizes
database_sizes = range(10, 101, 10)  # From 10 to 100, step by 10

# Store execution times
client_times = []
server_times = []

for size in database_sizes:
    client = Client(1024)
    server = Server(size)

    # Randomly select an index of interest
    index_of_interest = random.randint(0, size - 1)

    # Time for client to generate the request
    start_time = time.time()
    request_vector, public_key = client.request(size, index_of_interest)
    client_time = time.time() - start_time
    client_times.append(client_time)

    # Time for server to process the request
    start_time = time.time()
    encrypted_answer = server.answerRequest(request_vector, public_key)
    server_time = time.time() - start_time
    server_times.append(server_time)

    # Client decrypts the received answer (not timed as part of the PIR protocol execution time)
    decrypted_answer = client.decryptAnswer(encrypted_answer)

    # Verify that the decrypted answer matches the value in the server's database at the index of interest
    assert decrypted_answer == server.database[index_of_interest], "The PIR protocol failed to retrieve the correct value."

# Plotting the results
plt.plot(database_sizes, client_times, label='Client Time', marker='o')
plt.plot(database_sizes, server_times, label='Server Time', marker='s')

plt.xlabel('Database Size')
plt.ylabel('Execution Time (seconds)')
plt.title('PIR Protocol Execution Times')
plt.legend()
plt.grid(True)
plt.show()