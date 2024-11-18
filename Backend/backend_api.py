from flask import Flask, request, jsonify
from blockchain import Blockchain
from transaction import Transaction
from spv_client import SPVClient

app = Flask(__name__)

# Initialize blockchain and SPV client
blockchain = Blockchain()
spv_client = SPVClient(blockchain)

@app.route('/add_block', methods=['POST'])
def add_block():
    try:
        data = request.json
        transactions = [
            Transaction(
                txid=tx["txid"],
                inputs=tx["inputs"],
                outputs=tx["outputs"]
            )
            for tx in data["transactions"]
        ]
        previous_hash = blockchain.chain[-1].header["block_hash"]
        block = blockchain.create_block(transactions=transactions, previous_hash=previous_hash)
        blockchain.add_block_to_chain(block)
        return jsonify({"message": "Block added successfully", "block_hash": block.header["block_hash"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify_transaction', methods=['POST'])
def verify_transaction():
    try:
        data = request.json
        txid = data["txid"]
        block = blockchain.chain[-1]
        result = spv_client.verify_transaction(block=block, txid=txid)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
