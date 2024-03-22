import time
import random
import matplotlib.pyplot as plt
from client import Client
from server import Server
from utils import int_to_bytes

# Function to calculate the size in bits of the encrypted communication
def calculate_communication_size(encrypted_data):
    if isinstance(encrypted_data, list):
        # If it's a list, calculate the size of each encrypted element and sum them
        total_size = sum(len(int_to_bytes(data).hex()) * 4 for data in encrypted_data)  # Each hex digit represents 4 bits
    else:
        # If it's a single integer, just calculate its size
        total_size = len(int_to_bytes(encrypted_data).hex()) * 4
    return total_size

# Define the range of database sizes
database_sizes = range(10, 101, 10)  # From 10 to 100, step by 10

# Store communication sizes
client_to_server_comm_sizes = []
server_to_client_comm_sizes = []

for size in database_sizes:
    client = Client(1024)
    server = Server(size)

    # Randomly select an index of interest
    index_of_interest = random.randint(0, server.size - 1)

    # Client makes a request and measures communication size to server
    request_vector, public_key = client.request(size, index_of_interest)
    client_to_server_comm_sizes.append(calculate_communication_size(request_vector) + calculate_communication_size(public_key[0]) + calculate_communication_size(public_key[1]))

    # Server processes the request and measures communication size to client
    encrypted_answer = server.answerRequest(request_vector, public_key)
    server_to_client_comm_sizes.append(calculate_communication_size(encrypted_answer))

# Plotting the results
plt.plot(database_sizes, client_to_server_comm_sizes, label='Client to Server Communication Size', marker='o')
plt.plot(database_sizes, server_to_client_comm_sizes, label='Server to Client Communication Size', marker='s')

plt.xlabel('Database Size')
plt.ylabel('Communication Size (bits)')
plt.title('Communication Sizes for PIR Protocol')
plt.legend()
plt.grid(True)
plt.show()
