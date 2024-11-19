class Transaction:
    def __init__(self, txid, inputs, outputs):
        self.txid = txid
        self.inputs = inputs
        self.outputs = outputs

    def to_string(self):
        return f"{self.txid}:{self.inputs}:{self.outputs}"

    def __repr__(self):
        return f"Transaction(txid={self.txid}, inputs={self.inputs}, outputs={self.outputs})"

    @staticmethod
    def from_dict(tx_data):
        # Assuming tx_data is a dictionary representation of the transaction
        return Transaction(
            txid=tx_data['txid'],
            inputs=tx_data['inputs'],
            outputs=tx_data['outputs']
        )

    def to_dict(self):
        # Convert the transaction object to a dictionary
        return {
            'txid': self.txid,
            'inputs': self.inputs,
            'outputs': self.outputs
        }