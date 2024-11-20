# full_node.py
class FullNode:
    def __init__(self):
        self.name = "Full Node"

    def provide_block_header(self, tx_id):
        print(f"[Full Node] Responding with block header for tx_id: {tx_id}")
        return {
            "block_hash": "abcdef12345",
            "previous_hash": "1234xyz",
            "timestamp": "1632520830"
        }

    def provide_merkle_proof(self, tx_id, block_hash):
        print(f"[Full Node] Responding with Merkle proof for tx_id: {tx_id}")
        return {
            "path": ["abcdef12345", "1234xyz", "root_hash"],
            "transaction": tx_id
        }
