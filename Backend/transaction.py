class Transaction:
    def __init__(self, txid, inputs, outputs):
        self.txid = txid
        self.inputs = inputs
        self.outputs = outputs

    def to_string(self):
        return f"{self.txid}:{self.inputs}:{self.outputs}"

    def __repr__(self):
        return f"Transaction(txid={self.txid}, inputs={self.inputs}, outputs={self.outputs})"
