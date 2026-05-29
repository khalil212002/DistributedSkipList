import random
import env
import time
import os
import string
from p2p import Client
from store import Store


def get_random_string(length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def run_simulation():
    # Delay to allow servers to start up and connect to each other
    delay = int(os.getenv("STARTUP_DELAY", 15))
    print(f"Waiting {delay} seconds for nodes to initialize...")
    time.sleep(delay)

    # Load environment variables
    env.load()

    # In Docker Compose, we use the service name as the host
    # Defaulting to site1:8000 if not specified
    target_host = os.getenv("TARGET_HOST", f"site1:8000")
    print(f"Connecting to entry node at {target_host}...")

    client = Client(target_host, isServer=False)

    print("\n--- Inserting Random Store Objects ---")
    inserted_keys = []

    # Insert 10 random Store objects
    for _ in range(10):
        key = get_random_string(6)
        value = f"value_for_{key}"
        store_obj = Store(key, value)
        print(f"Sending INSERT for key: {key}")
        try:
            hops = client.sendInsert(store_obj, hops=0)
            print(f"  -> Inserted '{key}' successfully! (Took {hops} hops)")
            inserted_keys.append(key)
        except Exception as e:
            print(f"  -> Failed to insert '{key}'. Error: {e}")

    print("\n--- Searching for Inserted Data ---")
    # Pick a few items we just inserted to search for them
    sample_to_search = random.sample(inserted_keys, min(5, len(inserted_keys)))
    for key in sample_to_search:
        print(f"Sending SEARCH for key: {key}")
        try:
            # We search using a Store object with the same key
            result, hops = client.sendSearch(Store(key, ""), hops=0)
            if result is not None:
                print(
                    f"  -> Found! Key: {result.key}, Value: {result.value} (Took {hops} hops)"
                )
            else:
                print(
                    f"  -> Not found?! This shouldn't happen for '{key}'. (Took {hops} hops)"
                )
        except Exception as e:
            print(f"  -> Failed to search '{key}'. Error: {e}")

    print("\n--- Searching for Non-Existent Data ---")
    # Search for data we know isn't there
    for key in ["missing_one", "unknown_user", "not_in_list"]:
        print(f"Sending SEARCH for key: {key}")
        try:
            result, hops = client.sendSearch(Store(key, ""), hops=0)
            if result is not None:
                print(
                    f"  -> Found! Key: {result.key}, Value: {result.value} (Took {hops} hops)"
                )
            else:
                print(f"  -> Not found as expected for '{key}'! (Took {hops} hops)")
        except Exception as e:
            print(f"  -> Failed to search '{key}'. Error: {e}")

    print("\nSimulation complete.")
    client.close()


if __name__ == "__main__":
    run_simulation()
