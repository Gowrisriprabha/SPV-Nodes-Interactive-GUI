import hashlib

class MerkleTree:
    @staticmethod
    def generate_merkle_root(transactions):
        current_level = [MerkleTree.hash_transaction(tx) for tx in transactions]

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = left + right
                next_level.append(MerkleTree.double_hash(combined))
            current_level = next_level

        return current_level[0] if current_level else None

    @staticmethod
    def hash_transaction(transaction):
        tx_string = transaction.to_string()
        return MerkleTree.double_hash(tx_string)

    @staticmethod
    def double_hash(data):
        return hashlib.sha256(hashlib.sha256(data.encode()).digest()).hexdigest()
