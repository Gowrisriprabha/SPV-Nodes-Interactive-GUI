from flask import Flask, request, jsonify
from blockchain import Blockchain
from transaction import Transaction
from spv_client import SPVClient
from merkle_tree import MerkleTree

app = Flask(__name__)

# Initialize blockchain and SPV client
blockchain = Blockchain()
spv_client = SPVClient(blockchain)

@app.route('/create_block', methods=['POST'])
def create_block():
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
        previous_hash = data.get("previous_hash", blockchain.chain[-1].header["block_hash"])

        # Create and add the block
        block = blockchain.create_block(transactions=transactions, previous_hash=previous_hash)
        blockchain.add_block_to_chain(block)

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
    try:
        # Parse query parameters
        txid = request.args.get("tx_id")
        block_index = request.args.get("block_index", type=int)

        if not txid:
            return jsonify({"error": "Transaction ID (tx_id) is required"}), 400

        # Get the block by index or default to the latest block
        if block_index is not None:
            if block_index < 0 or block_index >= len(blockchain.chain):
                return jsonify({"error": f"Block index {block_index} is out of range"}), 404
            block = blockchain.chain[block_index]
        else:
            block = blockchain.chain[-1]

        # Verify the transaction in the block
        result = spv_client.verify_transaction(txid=txid, block=block)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
