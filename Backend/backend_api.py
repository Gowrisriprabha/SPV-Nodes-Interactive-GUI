import json
import time
from flask import Flask, request, jsonify
from block import Block
from blockchain import Blockchain
from transaction import Transaction
from spv_client import SPVClient
from merkle_tree import MerkleTree

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Heroku!"

# Initialize blockchain and SPV client
blockchain = Blockchain()
spv_client = SPVClient(blockchain)

# Function to load the blockchain from a JSON file
def load_blockchain_data():
    try:
        with open('blockchain_data.json', 'r') as file:
            data = json.load(file)
            blockchain.chain = [Block.from_dict(block) for block in data]
            print(f"Blockchain loaded from blockchain_data.json with {len(blockchain.chain)} blocks.")
    except FileNotFoundError:
        print("No existing blockchain data found. Starting fresh.")
        blockchain.chain = []  # Start with an empty chain if the file doesn't exist

# Function to save the blockchain to a JSON file
def save_blockchain_data():
    with open('blockchain_data.json', 'w') as file:
        json.dump([block.to_dict() for block in blockchain.chain], file)
        print(f"Blockchain saved to blockchain_data.json with {len(blockchain.chain)} blocks.")

def populate_blockchain():
    transactions = [
        {"txid": "tx1", "sender": "Alice", "receiver": "Bob", "amount": 50, "timestamp": int(time.time())},
        {"txid": "tx2", "sender": "Charlie", "receiver": "Diana", "amount": 75, "timestamp": int(time.time())},
    ]

    # Create Transaction objects
    transaction_objects = [
        Transaction(
            txid=tx["txid"],
            inputs=tx.get("inputs", []),
            outputs=tx.get("outputs", [])
        )
        for tx in transactions
    ]

    # Previous hash: Hash of the last block in the chain (if chain exists), otherwise for the genesis block
    if blockchain.chain:
        previous_hash = blockchain.chain[-1].block_hash
    else:
        previous_hash = "0" * 64  # All zeros for the genesis block

    # Current timestamp
    timestamp = int(time.time())

    # Calculate Merkle root for the transactions
    merkle_root = blockchain.calculate_merkle_root(transaction_objects)

    # Block data dictionary for hash calculation
    block_data = {
        "index": len(blockchain.chain),
        "previous_hash": previous_hash,
        "transactions": transactions,  # List of transaction dictionaries
        "timestamp": timestamp,
        "merkle_root": merkle_root,
    }

    # Calculate the block hash
    block_hash = blockchain.calculate_block_hash(block_data)

    print(f"Transactions in the block: {transactions}")
    # Create the block with all required parameters
    block = blockchain.create_block(transaction_objects, previous_hash, timestamp, merkle_root, block_hash)

    # Add the block to the blockchain
    blockchain.add_block_to_chain(block)
    print(f"Blockchain after initialization: {blockchain.chain}")
    print(f"Block added to the blockchain: {block}")


# Call the function to load blockchain data at the start of the app
populate_blockchain() 
print("Loaded")

@app.route('/create_block', methods=['POST'])
def create_block():
    try:
        # Parse JSON input
        data = request.json
        print(f"Received data: {data}")
        transactions = [
            Transaction(
                txid=tx["txid"],
                inputs=tx.get("inputs", []),
                outputs=tx.get("outputs", [])
            )
            for tx in data.get("transactions", [])
        ]
        print(f"Parsed transactions: {transactions}") 
        previous_hash = data.get("previous_hash", blockchain.chain[-1].header["block_hash"])
        print(f"Previous hash: {previous_hash}")

        # Create and add the block
        block = blockchain.create_block(transactions=transactions, previous_hash=previous_hash)
        blockchain.add_block_to_chain(block)

        # Save blockchain data after creating the block
        save_blockchain_data()

        return jsonify({
            "message": "Block created successfully",
            "block_hash": block.header["block_hash"],
            "merkle_root": block.header["merkle_root"],
            "transactions": [tx.to_dict() for tx in block.transactions],
            "index": len(blockchain.chain) - 1
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/verify_transaction', methods=['GET'])
def verify_transaction():
    tx_id = request.args.get('tx_id')
    block_index = int(request.args.get('block_index'))

    # Check block index range
    if block_index >= len(blockchain.chain):
        return {"error": "Block index out of range"}, 400

    # Retrieve block and ensure it's not empty
    block = blockchain.chain[block_index]
    print(f"Retrieved block: {block}")

    if not block.transactions:
        return {"message": "No transactions in the block"}, 404

    # Search for the transaction
    for transaction in block.transactions:
        if hasattr(transaction, 'txid') and transaction.txid == tx_id:
            return {"message": "Transaction found", "transaction": vars(transaction)}, 200

    return {"message": "Transaction not found"}, 404



@app.route('/generate_merkle_proof', methods=['GET'])
def generate_merkle_proof():
    try:
        # Parse query parameters
        txid = request.args.get("tx_id")
        block_index = request.args.get("block_index", type=int)

        if not txid:
            return jsonify({"error": "Transaction ID (tx_id) is required"}), 400

        # Get the block by index
        if block_index is None or block_index < 0 or block_index >= len(blockchain.chain):
            return jsonify({"error": f"Block index {block_index} is out of range"}), 404
        block = blockchain.chain[block_index]

        # Generate Merkle proof
        transaction_index = next((i for i, tx in enumerate(block.transactions) if tx.txid == txid), None)
        if transaction_index is None:
            return jsonify({"error": "Transaction not found in block"}), 404

        proof = spv_client.generate_merkle_proof(block.transactions, transaction_index)
        return jsonify({
            "transaction_hash": MerkleTree.hash_transaction(block.transactions[transaction_index]),
            "proof": proof,
            "merkle_root": block.header["merkle_root"]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/verify_merkle_proof', methods=['POST'])
def verify_merkle_proof():
    try:
        # Parse JSON input
        data = request.json
        transaction_hash = data.get("transaction_hash")
        proof = data.get("proof")
        merkle_root = data.get("merkle_root")

        if not transaction_hash or not proof or not merkle_root:
            return jsonify({"error": "transaction_hash, proof, and merkle_root are required"}), 400

        # Validate the Merkle proof
        is_valid = spv_client.validate_merkle_proof(transaction_hash, proof, merkle_root)
        return jsonify({"is_valid": is_valid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tamper_block', methods=['POST'])
def tamper_block():
    try:
        # Parse JSON input
        data = request.json
        block_index = data.get("block_index")
        new_amount = data.get("new_amount")

        if block_index is None or block_index < 0 or block_index >= len(blockchain.chain):
            return jsonify({"error": f"Block index {block_index} is out of range"}), 404

        if new_amount is None:
            return jsonify({"error": "new_amount is required"}), 400

        # Tamper with the block
        block = blockchain.chain[block_index]
        if not block.transactions:
            return jsonify({"error": "Block contains no transactions to tamper with"}), 400

        # Modify the first transaction's output
        block.transactions[0].outputs[0]["amount"] = new_amount

        # Recalculate the block hash
        block.header["block_hash"] = block.calculate_block_hash()

        # Save blockchain data after tampering the block
        save_blockchain_data()

        return jsonify({
            "message": "Block tampered successfully",
            "new_block_hash": block.header["block_hash"]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/calculate_merkle_root', methods=['POST'])
def calculate_merkle_root():
    try:
        # Parse JSON input
        data = request.json
        transactions = [
            Transaction(
                txid=tx["txid"],
                inputs=tx.get("inputs", []),
                outputs=tx.get("outputs", [])
            )
            for tx in data.get("transactions", [])
        ]
        merkle_root = MerkleTree.generate_merkle_root(transactions)
        expected_root = MerkleTree.hash_transaction(transactions[0]) if len(transactions) == 1 else merkle_root
        return jsonify({"merkle_root": merkle_root, "expected_root": expected_root}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))