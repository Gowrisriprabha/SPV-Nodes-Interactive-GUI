import hashlib
from transaction import Transaction

"""class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, block_hash=None, merkle_root=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.block_hash = block_hash
        self.merkle_root = merkle_root
        self.nonce = 0  # Default nonce value

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

    @staticmethod
    def from_dict(block_data):
        # Assuming 'block_data' is a dictionary representation of the block
        transactions = [Transaction.from_dict(tx) for tx in block_data['transactions']]
        return Block(
            index=block_data['index'],
            previous_hash=block_data['previous_hash'],
            transactions=transactions,
            timestamp=block_data['timestamp'],
            block_hash=block_data['block_hash'],
            merkle_root=block_data['merkle_root']
        )

    def to_dict(self):
        # Convert the block object to a dictionary
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'block_hash': self.block_hash,
            'merkle_root': self.merkle_root
        }
"""

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, block_hash, merkle_root):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.block_hash = block_hash
        self.merkle_root = merkle_root

    def __str__(self):
        return f"Block {self.index}: {self.transactions}"
    
    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.__dict__ if isinstance(tx, Transaction) else tx for tx in self.transactions],
            "timestamp": self.timestamp,
            "hash": self.block_hash
        }