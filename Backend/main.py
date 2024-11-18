import random
from blockchain import Blockchain
from transaction import Transaction
from spv_client import SPVClient
from time import sleep

# Simulate network request with a delay (for demonstration)
def simulate_network_request(delay=1):
    print("Sending request to full node...")
    sleep(delay)
    print("Response received from full node.")

# The main process for SPV verification with network simulation
def spv_verification_process(spv_instance, transaction_id, delay=1):
    simulate_network_request(delay)
    result = spv_instance.verify_transaction(transaction_id)
    if result.get("verified"):
        print(f"Transaction {transaction_id} verified.")
        return True, result
    else:
        print(f"Transaction {transaction_id} not found.")
        return False, None

if __name__ == "__main__":
    # Initialize blockchain
    blockchain = Blockchain()

    # Creating sample transactions
    transactions = [
        Transaction(
            txid=f"tx_{i}",
            inputs=[{"txid": "prev_tx", "output_index": 0}],
            outputs=[{"address": f"address_{i}", "amount": random.randint(1, 100)}]
        )
        for i in range(4)
    ]

    # Adding a new block with transactions
    block = blockchain.create_block(transactions=transactions, previous_hash=blockchain.chain[-1].header["previous_hash"])
    blockchain.add_block_to_chain(block)

    # Initialize SPV client
    spv_client = SPVClient(blockchain)

    # Transaction ID to verify
    txid_to_verify = "tx_0"

    # Perform SPV verification
    print("Starting SPV verification process...")
    is_verified, result = spv_verification_process(spv_client, txid_to_verify)

    # Output the verification result
    if is_verified:
        print("SPV Verification Result:")
        print(f"Transaction Hash: {result['transaction_hash']}")
        print(f"Merkle Proof: {result['proof']}")
        print(f"Merkle Root: {result['merkle_root']}")
        print(f"Verification Status: {'Verified' if result['verified'] else 'Verification Failed'}")
    else:
        print("Verification failed. The transaction could not be found.")
