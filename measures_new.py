import time
import matplotlib.pyplot as plt
from client_new import Client
from server_new import Server, random
from utils import int_to_bytes
from time_db_size import client_times as client_times_1d, server_times as server_times_1d
from size_communications import client_to_server_comm_sizes as comm_sizes_client_1d, server_to_client_comm_sizes as comm_sizes_server_1d


# Function to calculate the size in bits of the encrypted communication
def calculate_communication_size(encrypted_data):
    if isinstance(encrypted_data, list):
        # If it's a list of encrypted numbers, sum their bit sizes
        return sum(len(int_to_bytes(data)) * 8 for data in encrypted_data)
    else:
        # Single encrypted number's bit size
        return len(int_to_bytes(encrypted_data)) * 8

# Assume max_elements is the maximum size of your 1D databases
max_elements = 100  # This should be the square of the max 2D database dimension
database_dimensions = [(i, i) for i in range(1, int(max_elements ** 0.5) + 1)]

# Store metrics
client_times_2d = []
server_times_2d = []
comm_sizes_client_2d = []
comm_sizes_server_2d = []

for N, M in database_dimensions:
    # Initialize client and server for a 2D database
    client = Client(1024)
    server = Server(N, M)

    # Select random row and column indices of interest
    row_index = random.randint(0, N - 1)
    col_index = random.randint(0, M - 1)

    # Measure client request generation time and size
    start_time = time.time()
    request_vectors, public_key = client.request(N, M, row_index, col_index)
    client_time = time.time() - start_time
    client_comm_size = calculate_communication_size(request_vectors[0]) + calculate_communication_size(request_vectors[1])
    
    # Measure server processing time and response size
    start_time = time.time()
    encrypted_answers = server.answerRequest(request_vectors, public_key)
    server_time = time.time() - start_time
    server_comm_size = calculate_communication_size(encrypted_answers)

    # Append to metrics lists
    client_times_2d.append(client_time)
    server_times_2d.append(server_time)
    comm_sizes_client_2d.append(client_comm_size)
    comm_sizes_server_2d.append(server_comm_size)

# Database sizes (for plotting)
database_sizes = [N * M for N, M in database_dimensions]

# Plotting execution times
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
plt.plot(database_sizes, client_times_2d, 'o-', label='2D Client Time')
plt.plot(database_sizes, server_times_2d, 's-', label='2D Server Time')
plt.plot(database_sizes, client_times_1d, 'o--', label='1D Client Time')
plt.plot(database_sizes, server_times_1d, 's--', label='1D Server Time')
plt.xlabel('Database Size (elements)')
plt.ylabel('Execution Time (seconds)')
plt.title('PIR Protocol Execution Time Comparison')
plt.legend()
plt.grid(True)

# Plotting communication sizes
plt.subplot(1, 2, 2)
plt.plot(database_sizes, comm_sizes_client_2d, 'o-', label='2D Client to Server Comm Size')
plt.plot(database_sizes, comm_sizes_server_2d, 's-', label='2D Server to Client Comm Size')
plt.plot(database_sizes, comm_sizes_client_1d, 'o--', label='1D Client to Server Comm Size')
plt.plot(database_sizes, comm_sizes_server_1d, 's--', label='1D Server to Client Comm Size')
plt.xlabel('Database Size (elements)')
plt.ylabel('Communication Size (bits)')
plt.title('PIR Protocol Communication Size Comparison')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
