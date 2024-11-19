from datetime import datetime
from merkle_tree import MerkleTree
from block import Block
import hashlib
import time

"""class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.create_genesis_block()  
        self.difficulty = difficulty
        self.create_genesis_block()

    def calculate_block_hash(self, block_data):
        #Calculate the hash for a block using block data.
        block_string = f"{block_data['index']}{block_data['previous_hash']}{block_data['transactions']}{block_data['timestamp']}{block_data['merkle_root']}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def create_genesis_block(self):
        #Create the genesis block.
        transactions = []  # No transactions for genesis block
        previous_hash = "0" * 64  # Genesis block has no previous block, so set previous hash to all zeros
        timestamp = int(time.time())  # Current time as timestamp
        merkle_root = self.calculate_merkle_root(transactions)  # Calculate the Merkle root (or set manually)

        # Create block data dictionary to pass into the block creation
        block_data = {
            'index': 0,
            'previous_hash': previous_hash,
            'transactions': transactions,
            'timestamp': timestamp,
            'merkle_root': merkle_root
        }
        
        # Calculate the block hash for the genesis block
        block_hash = self.calculate_block_hash(block_data)
        
        # Create the genesis block
        genesis_block = self.create_block(transactions, previous_hash, timestamp, merkle_root, block_hash)
        
        # Add the genesis block to the chain
        self.chain.append(genesis_block)

    def create_block(self, transactions, previous_hash, timestamp, merkle_root, block_hash):
        #Create a block and return it.
        index = len(self.chain)

        # Create the block using all necessary arguments
        block = Block(
            index=index,
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            block_hash=block_hash,
            merkle_root=merkle_root
        )
        return block

    def add_block_to_chain(self, block):
        self.chain.append(block)

    def get_block_by_txid(self, txid):
        #Get the block containing a transaction by txid
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.txid == txid:
                    return block
        return None

    def get_merkle_root(self, block):
        #Returns the Merkle root for the given block.
        return block.header["merkle_root"]

    def calculate_merkle_root(self, transactions):
        #A simple example of Merkle Root calculation.
        if len(transactions) == 0:
            return ""
        if len(transactions) == 1:
            return transactions[0]["txid"]  # Access 'txid' from dictionary
    
        while len(transactions) > 1:
            # Combine pairs of transaction hashes
            temp = []
            for i in range(0, len(transactions), 2):
                if i + 1 < len(transactions):
                    combined = transactions[i]["txid"] + transactions[i + 1]["txid"]
                else:
                    combined = transactions[i]["txid"]  # Handle odd count of transactions
                temp.append(hashlib.sha256(combined.encode()).hexdigest())
            # Update transactions with the new layer of hashes
            transactions = [{"txid": hash} for hash in temp]
    
        return transactions[0]["txid"]

    def hash_transaction(self, transaction):
        # Create a hash of the transaction (for simplicity, just hash the string representation)
        tx_string = str(transaction)
        return self.hash_string(tx_string)

    def hash_string(self, string):
        return hashlib.sha256(string.encode()).hexdigest() """
    
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create genesis block (index 0)
        genesis_block = Block(
            index=0,
            previous_hash="0" * 64,
            transactions=[],  # Empty transactions for the genesis block
            timestamp=int(time.time()),
            block_hash="0000000000000000000000000000000000000000000000000000000000000000",
            merkle_root="",
        )
        self.chain.append(genesis_block)

    def calculate_merkle_root(self, transactions):
        # Placeholder for calculating the Merkle root (you can use a proper Merkle tree)
        tx_hashes = [self.calculate_block_hash(tx) for tx in transactions]
        while len(tx_hashes) > 1:
            # Pair hashes and compute hash of pairs until one hash remains
            tx_hashes = [self.calculate_block_hash(tx_hashes[i] + tx_hashes[i + 1]) if i + 1 < len(tx_hashes) else tx_hashes[i] for i in range(0, len(tx_hashes), 2)]
        return tx_hashes[0]  # Final Merkle root

    def calculate_block_hash(self, data):
        # Calculate block hash using SHA-256
        return hashlib.sha256(str(data).encode()).hexdigest()

    def create_block(self, transactions, previous_hash, timestamp, merkle_root, block_hash):
        return Block(
            index=len(self.chain),
            previous_hash=previous_hash,
            transactions=transactions,
            timestamp=timestamp,
            block_hash=block_hash,
            merkle_root=merkle_root,
        )

    def add_block_to_chain(self, block):
        self.chain.append(block)