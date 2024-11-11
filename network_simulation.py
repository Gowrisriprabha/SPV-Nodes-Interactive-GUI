import time


def simulate_network_request(delay=1):
    print("Sending request to full node...")
    time.sleep(delay)
    print("Response received from full node.")
