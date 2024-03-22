import random

class Server:
    def __init__(self, db_rows, db_columns):
        # Create a 2D database with random values
        self.database = [[random.randint(1, 2**16) for _ in range(db_columns)] for _ in range(db_rows)]

    def answerRequest(self, request_vectors, public_key):
        row_vector, col_vector = request_vectors
        n, g = public_key
        n_sq = n**2
        encrypted_answers = []

        # Compute the encrypted answers for each column
        for col in range(len(self.database[0])):
            encrypted_sum = pow(g, 0, n_sq)  # Initialize to Enc(0)
            for row in range(len(self.database)):
                # Homomorphically compute the encrypted value
                encrypted_value = pow(row_vector[row], self.database[row][col], n_sq)
                # Add the value to the encrypted sum for the column
                encrypted_sum = (encrypted_sum * encrypted_value) % n_sq
            # Store the result for the column
            encrypted_answers.append(encrypted_sum)

        # Return the encrypted answers for all columns
        return encrypted_answers
