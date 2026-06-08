import os
import time
import random
import csv
import matplotlib.pyplot as plt
from p2p import Client

# Configuration
TARGET_HOST = os.getenv("TARGET_HOST", "site1:8000")
STARTUP_DELAY = int(os.getenv("STARTUP_DELAY", "10"))
BATCH_SIZES = [100, 500, 1000, 5000]

# Define the output directory that is mapped to your host machine
OUTPUT_DIR = "/app/results"


def run_simulation():
    print(f"Waiting {STARTUP_DELAY} seconds for network to initialize...")
    time.sleep(STARTUP_DELAY)

    print(f"Connecting to entry node: {TARGET_HOST}")
    client = Client(TARGET_HOST)

    # Data storage
    results_data = []
    batches, avg_insert_times, avg_search_times = [], [], []
    avg_insert_hops_data, avg_search_hops_data, error_rates = [], [], []
    current_key_space = set()

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for batch_size in BATCH_SIZES:
        print(f"\n--- Starting Batch: {batch_size} Operations ---")

        # 1. Insertion Test
        insert_hops, insert_times, insert_errors = 0, [], 0
        for _ in range(batch_size):
            key = random.randint(1, 10000)
            start_time = time.time()
            try:
                hops = client.sendInsert(key)
                insert_hops += hops
                current_key_space.add(key)
            except Exception:
                insert_errors += 1
            insert_times.append(time.time() - start_time)

        # 2. Search Test
        search_hops, search_times, search_errors = 0, [], 0
        search_keys = (
            random.choices(list(current_key_space), k=batch_size)
            if current_key_space
            else []
        )
        for key in search_keys:
            start_time = time.time()
            try:
                result, hops = client.sendSearch(key)
                search_hops += hops
                if result is None:
                    search_errors += 1
            except Exception:
                search_errors += 1
            search_times.append(time.time() - start_time)

        # 3. Delete Test (10% of batch)
        delete_amount = max(1, batch_size // 10)
        delete_hops, delete_times, delete_errors = 0, [], 0
        delete_keys = (
            random.choices(list(current_key_space), k=delete_amount)
            if current_key_space
            else []
        )
        for key in delete_keys:
            start_time = time.time()
            try:
                hops = client.sendDelete(key)
                delete_hops += hops
                current_key_space.remove(key)
            except Exception:
                delete_errors += 1
            delete_times.append(time.time() - start_time)

        # Calculate Metrics
        avg_insert_time = sum(insert_times) / len(insert_times) if insert_times else 0
        avg_search_time = sum(search_times) / len(search_times) if search_times else 0
        avg_insert_hop = insert_hops / batch_size if batch_size else 0
        avg_search_hop = search_hops / batch_size if batch_size else 0

        total_ops = batch_size * 2 + delete_amount
        total_errors = insert_errors + search_errors + delete_errors
        error_rate = (total_errors / total_ops) * 100

        # Store for plotting & CSV
        results_data.append(
            {
                "Batch Size": batch_size,
                "Avg Insert Time (s)": round(avg_insert_time, 5),
                "Avg Search Time (s)": round(avg_search_time, 5),
                "Avg Insert Hops": round(avg_insert_hop, 2),
                "Avg Search Hops": round(avg_search_hop, 2),
                "Error Rate (%)": round(error_rate, 2),
            }
        )

        batches.append(batch_size)
        avg_insert_times.append(avg_insert_time)
        avg_search_times.append(avg_search_time)
        avg_insert_hops_data.append(avg_insert_hop)
        avg_search_hops_data.append(avg_search_hop)
        error_rates.append(error_rate)

    print("\nSimulation complete. Saving results...")

    # --- Save CSV Data ---
    csv_file = os.path.join(OUTPUT_DIR, "simulation_results.csv")
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results_data[0].keys())
        writer.writeheader()
        writer.writerows(results_data)

    # --- Save Graph Image ---
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].plot(
        batches, avg_insert_hops_data, label="Insert Hops", marker="o", color="blue"
    )
    axs[0].plot(
        batches, avg_search_hops_data, label="Search Hops", marker="x", color="cyan"
    )
    axs[0].set_title("Average Network Hops vs Batch Size")
    axs[0].set_xlabel("Batch Size (Operations)")
    axs[0].set_ylabel("Average Hops")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(
        batches, avg_insert_times, label="Insert Time (s)", marker="o", color="red"
    )
    axs[1].plot(
        batches, avg_search_times, label="Search Time (s)", marker="x", color="orange"
    )
    axs[1].set_title("Average Operation Latency vs Batch Size")
    axs[1].set_xlabel("Batch Size (Operations)")
    axs[1].set_ylabel("Time (Seconds)")
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(batches, error_rates, label="Error Rate (%)", marker="s", color="green")
    axs[2].set_title("Error Rate vs Batch Size")
    axs[2].set_xlabel("Batch Size (Operations)")
    axs[2].set_ylabel("Error Rate (%)")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()

    # Save the plot instead of showing it
    png_file = os.path.join(OUTPUT_DIR, "simulation_graphs.png")
    plt.savefig(png_file)
    print(f"Data saved to {csv_file}")
    print(f"Graphs saved to {png_file}")


if __name__ == "__main__":
    run_simulation()
