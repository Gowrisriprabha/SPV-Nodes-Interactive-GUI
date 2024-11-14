import hashlib

class Block:
    def __init__(self, header, transactions):
        self.header = header
        self.transactions = transactions

    def calculate_block_hash(self):
        block_string = f"{self.header['version']}{self.header['previous_hash']}{self.header['merkle_root']}{self.header['timestamp']}{self.header['nonce']}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty):
        while True:
            block_hash = self.calculate_block_hash()
            if block_hash.startswith("0" * difficulty):
                self.header["block_hash"] = block_hash
                break
            self.header["nonce"] += 1
