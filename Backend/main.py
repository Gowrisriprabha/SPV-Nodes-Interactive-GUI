import random
from blockchain import Blockchain
from transaction import Transaction
from spv_client import SPVClient

if __name__ == "__main__":
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
    block = blockchain.create_block(transactions=transactions, previous_hash=blockchain.chain[-1].header["block_hash"])
    blockchain.add_block_to_chain(block)

    # SPV verification
    spv_client = SPVClient(blockchain)
    result = spv_client.verify_transaction(block=blockchain.chain[-1], txid="tx_0")

    # Output result of verification
    print("SPV Verification Result:")
    print(f"Transaction Hash: {result['transaction_hash']}")
    print(f"Merkle Proof: {result['proof']}")
    print(f"Merkle Root: {result['merkle_root']}")
    print(f"Verification Status: {'Verified' if result['verified'] else 'Verification Failed'}")
