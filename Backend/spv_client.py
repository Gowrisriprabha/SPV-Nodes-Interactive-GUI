from merkle_tree import MerkleTree

class SPVClient:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def verify_transaction(self, txid):
        block = self.blockchain.get_block_by_txid(txid)
        if block is None:
            return {"error": "Transaction not found in any block"}

        tx_index = next((i for i, tx in enumerate(block.transactions) if tx.txid == txid), None)
        if tx_index is None:
            return {"error": "Transaction not found in block"}

        tx_hash = MerkleTree.hash_transaction(block.transactions[tx_index])
        proof = self.generate_merkle_proof(block.transactions, tx_index)
        merkle_root = block.header["merkle_root"]

        verified = self.validate_merkle_proof(tx_hash, proof, merkle_root)
        return {
            "transaction_hash": tx_hash,
            "proof": proof,
            "merkle_root": merkle_root,
            "verified": verified
        }

    def generate_merkle_proof(self, transactions, tx_index):
        current_level = [MerkleTree.hash_transaction(tx) for tx in transactions]
        proof = []

        while len(current_level) > 1:
            sibling_index = tx_index + 1 if tx_index % 2 == 0 else tx_index - 1
            proof.append(current_level[sibling_index] if sibling_index < len(current_level) else current_level[tx_index])

            tx_index = tx_index // 2
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = left + right
                next_level.append(MerkleTree.double_hash(combined))
            current_level = next_level

        return proof

    def validate_merkle_proof(self, tx_hash, proof, merkle_root):
        hash_val = tx_hash
        for sibling in proof:
            combined = hash_val + sibling if hash_val < sibling else sibling + hash_val
            hash_val = MerkleTree.double_hash(combined)
        return hash_val == merkle_root

