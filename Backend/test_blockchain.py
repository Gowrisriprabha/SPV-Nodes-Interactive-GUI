import unittest
import requests
from datetime import datetime

class TestBlockchainBoundaryCasesFrontend(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api"  # Update this URL to match your frontend API endpoint

    def test_empty_transaction_list(self):
        # Test creating a block with no transactions through the API
        response = requests.post(f"{self.BASE_URL}/create_block", json={"transactions": []})
        self.assertEqual(response.status_code, 200, "API should return status 200 for valid request")
        data = response.json()
        self.assertEqual(len(data["transactions"]), 0, "Block should have no transactions")
        self.assertIsNone(data["merkle_root"], "Merkle root should be None for empty transaction list")

    def test_invalid_transaction_id(self):
        # Test verifying a non-existent transaction ID
        response = requests.get(f"{self.BASE_URL}/verify_transaction", params={"tx_id": "invalid_tx"})
        self.assertEqual(response.status_code, 404, "Should return 404 for non-existent transaction ID")
        data = response.json()
        self.assertIn("error", data, "Should return error in response")
        self.assertEqual(data["error"], "Transaction not found", "Error message should match expected")

    def test_invalid_merkle_proof(self):
        # Test tampered Merkle proof verification
        transactions = [{"txid": f"tx_{i}", "outputs": [{"address": f"address_{i}", "amount": 10}]} for i in range(2)]
        create_block_response = requests.post(f"{self.BASE_URL}/create_block", json={"transactions": transactions})
        self.assertEqual(create_block_response.status_code, 200, "Block creation should be successful")
        block_data = create_block_response.json()

        valid_txid = transactions[1]["txid"]
        proof_response = requests.get(f"{self.BASE_URL}/generate_merkle_proof", params={"tx_id": valid_txid})
        self.assertEqual(proof_response.status_code, 200, "Proof generation should succeed")
        proof_data = proof_response.json()

        # Tamper the proof
        tampered_proof = proof_data["proof"]
        tampered_proof[0] = "0" * 64  # Alter the proof with an invalid hash

        verify_response = requests.post(f"{self.BASE_URL}/verify_merkle_proof", json={
            "transaction_hash": proof_data["transaction_hash"],
            "proof": tampered_proof,
            "merkle_root": block_data["merkle_root"]
        })
        self.assertEqual(verify_response.status_code, 400, "Tampered proof should return error")
        self.assertFalse(verify_response.json()["is_valid"], "Tampered proof should fail validation")

    def test_invalid_block_hash_after_mining(self):
        # Test changing block data after mining
        transactions = [{"txid": "tx_2", "outputs": [{"address": "address_2", "amount": 100}]}]
        create_block_response = requests.post(f"{self.BASE_URL}/create_block", json={"transactions": transactions})
        self.assertEqual(create_block_response.status_code, 200, "Block creation should be successful")
        block_data = create_block_response.json()

        # Simulate tampering via frontend
        tamper_response = requests.post(f"{self.BASE_URL}/tamper_block", json={"block_index": block_data["index"], "new_amount": 9999})
        self.assertEqual(tamper_response.status_code, 400, "Tampering should be detected by the system")
        tampered_data = tamper_response.json()
        self.assertIn("error", tampered_data, "Response should include error for tampered block")

    def test_invalid_previous_hash_in_block(self):
        # Test adding a block with an invalid previous hash
        invalid_prev_hash = "0" * 64
        transactions = [{"txid": "tx_3", "outputs": [{"address": "address_3", "amount": 75}]}]
        response = requests.post(f"{self.BASE_URL}/create_block", json={
            "transactions": transactions,
            "previous_hash": invalid_prev_hash
        })
        self.assertEqual(response.status_code, 400, "Invalid previous hash should result in an error")
        data = response.json()
        self.assertIn("error", data, "Response should include error for invalid previous hash")

    def test_merkle_root_with_one_transaction(self):
        # Check Merkle root calculation for a single transaction
        transaction = {"txid": "tx_single", "outputs": [{"address": "address_1", "amount": 100}]}
        response = requests.post(f"{self.BASE_URL}/calculate_merkle_root", json={"transactions": [transaction]})
        self.assertEqual(response.status_code, 200, "Merkle root calculation should be successful")
        data = response.json()
        expected_root = data["expected_root"]
        self.assertEqual(data["merkle_root"], expected_root, "Merkle root should match expected")

    def test_merkle_proof_for_single_transaction(self):
        # Generate and validate Merkle proof for a single transaction
        transaction = {"txid": "tx_1", "outputs": [{"address": "address_1", "amount": 100}]}
        create_block_response = requests.post(f"{self.BASE_URL}/create_block", json={"transactions": [transaction]})
        self.assertEqual(create_block_response.status_code, 200, "Block creation should succeed")
        block_data = create_block_response.json()

        proof_response = requests.get(f"{self.BASE_URL}/generate_merkle_proof", params={"tx_id": transaction["txid"]})
        self.assertEqual(proof_response.status_code, 200, "Proof generation should succeed")
        proof_data = proof_response.json()

        verify_response = requests.post(f"{self.BASE_URL}/verify_merkle_proof", json={
            "transaction_hash": proof_data["transaction_hash"],
            "proof": proof_data["proof"],
            "merkle_root": block_data["merkle_root"]
        })
        self.assertTrue(verify_response.json()["is_valid"], "Single transaction proof should be valid")

if __name__ == "__main__":
    unittest.main()
