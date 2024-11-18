# test_blockchain.py
import unittest
from blockchain import blockchain
from transaction import transaction
from spv_client import spv_client
from block import block
from merkle_tree import merkle_tree

class TestBlockchainBoundaryCases(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.spv_client = SPVClient(self.blockchain)

    def test_empty_transaction_list(self):
        # Test creating a block with no transactions
        empty_block = self.blockchain.create_block([], self.blockchain.chain[-1].header["block_hash"])
        self.assertEqual(len(empty_block.transactions), 0, "Block should have no transactions")
        self.assertIsNone(empty_block.header["merkle_root"], "Merkle root should be None for empty transaction list")

    def test_invalid_transaction_id(self):
        # Test verifying a non-existent transaction ID
        transaction = Transaction("tx_1", [{"txid": "prev_tx", "output_index": 0}], [{"address": "address_1", "amount": 50}])
        block = self.blockchain.create_block([transaction], self.blockchain.chain[-1].header["block_hash"])
        self.blockchain.add_block_to_chain(block)
        result = self.spv_client.verify_transaction(block, "invalid_tx")
        self.assertIn("error", result, "Should return error for non-existent transaction ID")
        self.assertEqual(result["error"], "Transaction not found in block")

    def test_invalid_merkle_proof(self):
        # Test verification with a tampered Merkle proof
        transactions = [Transaction(f"tx_{i}", [], [{"address": f"address_{i}", "amount": 10}]) for i in range(2)]
        block = self.blockchain.create_block(transactions, self.blockchain.chain[-1].header["block_hash"])
        self.blockchain.add_block_to_chain(block)
        
        valid_txid = "tx_1"
        proof = self.spv_client.generate_merkle_proof(transactions, 1)
        
        tampered_proof = proof[:]
        tampered_proof[0] = "0" * 64  # Alter the proof with an invalid hash
        
        result = self.spv_client.verify_transaction(block, valid_txid)
        result["proof"] = tampered_proof
        is_valid = self.spv_client.validate_merkle_proof(result["transaction_hash"], tampered_proof, result["merkle_root"])
        self.assertFalse(is_valid, "Tampered proof should fail validation")

    def test_invalid_block_hash_after_mining(self):
        # Test changing block data after mining to verify hash mismatch
        transactions = [Transaction("tx_2", [{"txid": "prev_tx", "output_index": 0}], [{"address": "address_2", "amount": 100}])]
        block = self.blockchain.create_block(transactions, self.blockchain.chain[-1].header["block_hash"])
        self.blockchain.add_block_to_chain(block)
        
        # Tamper with block after mining
        block.transactions[0].outputs[0]["amount"] = 9999  # Change amount
        altered_hash = block.calculate_block_hash()
        
        self.assertNotEqual(block.header["block_hash"], altered_hash, "Block hash should mismatch after tampering")

    def test_invalid_previous_hash_in_block(self):
        # Attempt to add a block with an invalid previous hash
        invalid_prev_hash = "0" * 64
        transactions = [Transaction("tx_3", [], [{"address": "address_3", "amount": 75}])]
        block = Block({"version": "1.0", "previous_hash": invalid_prev_hash, "merkle_root": "dummy_root", "timestamp": "timestamp", "difficulty": 4, "nonce": 0}, transactions)

        with self.assertRaises(ValueError, msg="Should raise an error for invalid previous hash"):
            self.blockchain.add_block_to_chain(block)

    def test_merkle_root_with_one_transaction(self):
        # Check Merkle root calculation for a single transaction
        single_transaction = [Transaction("tx_single", [], [{"address": "address_1", "amount": 100}])]
        merkle_root = MerkleTree.generate_merkle_root(single_transaction)
        expected_root = MerkleTree.hash_transaction(single_transaction[0])
        self.assertEqual(merkle_root, expected_root, "Merkle root should equal the hash of the only transaction")

    def test_merkle_proof_for_single_transaction(self):
        # Generate and validate Merkle proof for a single transaction
        transactions = [Transaction("tx_1", [], [{"address": "address_1", "amount": 100}])]
        proof = self.spv_client.generate_merkle_proof(transactions, 0)
        tx_hash = MerkleTree.hash_transaction(transactions[0])
        merkle_root = MerkleTree.generate_merkle_root(transactions)
        self.assertTrue(self.spv_client.validate_merkle_proof(tx_hash, proof, merkle_root), "Single transaction proof should be valid")

    def test_invalid_merkle_root_in_block(self):
        # Verify that adding a block with a tampered Merkle root fails validation
        transactions = [Transaction("tx_invalid", [], [{"address": "address_invalid", "amount": 50}])]
        merkle_root = MerkleTree.generate_merkle_root(transactions)
        header = {
            "version": "1.0",
            "previous_hash": self.blockchain.chain[-1].header["block_hash"],
            "merkle_root": "tampered_root",
            "timestamp": datetime.now().isoformat(),
            "difficulty": self.blockchain.difficulty,
            "nonce": 0
        }
        block = Block(header, transactions)
        with self.assertRaises(ValueError, msg="Should raise an error for tampered Merkle root"):
            self.blockchain.add_block_to_chain(block)

if __name__ == "__main__":
    unittest.main()
