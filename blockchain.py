import hashlib
from datetime import datetime
from block import Block
from merkle_tree import MerkleTree

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.create_block([], '0' * 64)
        self.add_block_to_chain(genesis_block)

    def create_block(self, transactions, previous_hash):
        merkle_root = MerkleTree.generate_merkle_root(transactions)
        header = {
            "version": "1.0",
            "previous_hash": previous_hash,
            "merkle_root": merkle_root,
            "timestamp": datetime.now().isoformat(),
            "difficulty": self.difficulty,
            "nonce": 0
        }
        block = Block(header, transactions)
        block.mine(self.difficulty)
        return block

    def add_block_to_chain(self, block):
        self.chain.append(block)
