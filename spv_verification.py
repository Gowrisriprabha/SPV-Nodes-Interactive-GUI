def spv_verification_process(spv_instance, transaction_id, block, delay=1):
    simulate_network_request(delay)
    result = spv_instance.verify_transaction(block, transaction_id)
    if result.get("verified"):
        print(f"Transaction {transaction_id} verified.")
        return True, result
    else:
        print(f"Transaction {transaction_id} not found.")
        return False, None
