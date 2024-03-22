from paillier import Paillier

class Client:
    def __init__(self, bits):
        self.phe = Paillier(bits)

    def request(self, db_rows, db_columns, row_index, col_index):
        # Create two vectors for rows and columns
        row_vector = [self.phe.encrypt(0) for _ in range(db_rows)]
        col_vector = [self.phe.encrypt(0) for _ in range(db_columns)]

        # Encrypt 1 at the specified row and column indices
        row_vector[row_index] = self.phe.encrypt(1)
        col_vector[col_index] = self.phe.encrypt(1)

        # Return the row vector, column vector, and public key as the request
        return (row_vector, col_vector), self.phe.public_key

    def decryptAnswer(self, encrypted_answer):
        return self.phe.decrypt(encrypted_answer)
