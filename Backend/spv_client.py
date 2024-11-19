from merkle_tree import MerkleTree

class SPVClient:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def verify_transaction(self, block, txid):
        """
        Verifies a transaction in a specific block by checking its Merkle proof.
        
        Args:
            block (Block): The block containing the transaction.
            txid (str): The transaction ID to verify.
        
        Returns:
            dict: Verification result including the transaction hash, proof, 
                  Merkle root, and verification status.
        """
        # Locate transaction within the block
        tx_index = next((i for i, tx in enumerate(block.transactions) if tx.txid == txid), None)
        if tx_index is None:
            return {
                "error": "Transaction not found in block",
                "verified": False,
                "transaction_hash": None,
                "proof": None,
                "merkle_root": block.header.get("merkle_root"),
            }

        # Calculate transaction hash
        tx_hash = MerkleTree.hash_transaction(block.transactions[tx_index])

        # Generate Merkle proof
        proof = self.generate_merkle_proof(block.transactions, tx_index)

        # Fetch Merkle root from the block header
        merkle_root = block.header.get("merkle_root")

        # Validate the Merkle proof
        verified = self.validate_merkle_proof(tx_hash, proof, merkle_root)

        # Return result
        return {
            "transaction_hash": tx_hash,
            "proof": proof,
            "merkle_root": merkle_root,
            "verified": verified,
        }

    def generate_merkle_proof(self, transactions, tx_index):
        """
        Generates a Merkle proof for a given transaction in the transaction list.
        
        Args:
            transactions (list): The list of transactions in the block.
            tx_index (int): The index of the transaction for which the proof is generated.
        
        Returns:
            list: The Merkle proof as a list of sibling hashes.
        """
        current_level = [MerkleTree.hash_transaction(tx) for tx in transactions]
        proof = []

        while len(current_level) > 1:
            # Identify sibling index
            sibling_index = tx_index + 1 if tx_index % 2 == 0 else tx_index - 1

            # Append sibling hash to proof if it exists
            if sibling_index < len(current_level):
                proof.append(current_level[sibling_index])

            # Move up the tree
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
        """
        Validates a Merkle proof for a given transaction hash.
        
        Args:
            tx_hash (str): The hash of the transaction to validate.
            proof (list): The Merkle proof as a list of sibling hashes.
            merkle_root (str): The root hash of the Merkle tree.
        
        Returns:
            bool: True if the Merkle proof is valid, False otherwise.
        """
        hash_val = tx_hash

        for sibling in proof:
            # Combine hashes in lexicographical order
            combined = hash_val + sibling if hash_val < sibling else sibling + hash_val
            hash_val = MerkleTree.double_hash(combined)

        return hash_val == merkle_root
