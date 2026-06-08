import os
import time
import random
import csv
import matplotlib.pyplot as plt
from p2p import Client

TARGET_HOST = os.getenv("TARGET_HOST", "site1:8000")
STARTUP_DELAY = int(os.getenv("STARTUP_DELAY", "10"))
N_SIZES = [100, 500, 1000, 5000, 10000]

RESUTL_DIR = "/app/results"


def run_simulation():
    print(f"Waiting {STARTUP_DELAY} secs for p2p connecction to start.")
    time.sleep(STARTUP_DELAY)

    print(f"Connecting to: {TARGET_HOST}")
    cl = Client(TARGET_HOST)

    results_data = []
    n, avgInsetTime, avgSearchTime = [], [], []
    avgInsertHops, avgSearchHops, errRate = [], [], []
    createdKeys = set()

    os.makedirs(RESUTL_DIR, exist_ok=True)

    for nSize in N_SIZES:
        print(f"\n\nN: {nSize}")

        iHops, iTime, iError = 0, [], 0
        for _ in range(nSize):
            key = random.randint(1, 10000)
            startTime = time.time()
            try:
                hops = cl.sendInsert(key)
                iHops += hops
                createdKeys.add(key)
            except Exception:
                iError += 1
            iTime.append(time.time() - startTime)

        sHops, sTime, sError = 0, [], 0
        searchKeys = random.choices(list(createdKeys), k=nSize) if createdKeys else []
        for key in searchKeys:
            startTime = time.time()
            try:
                result, hops = cl.sendSearch(key)
                sHops += hops
                if result is None:
                    sError += 1
            except Exception:
                sError += 1
            sTime.append(time.time() - startTime)

        deleteAmount = max(1, nSize // 10)
        deleteHops, deleteTimes, deleteErrors = 0, [], 0
        deleteKeys = (
            random.choices(list(createdKeys), k=deleteAmount) if createdKeys else []
        )
        for key in deleteKeys:
            startTime = time.time()
            try:
                hops = cl.sendDelete(key)
                deleteHops += hops
                createdKeys.remove(key)
            except Exception:
                deleteErrors += 1
            deleteTimes.append(time.time() - startTime)

        avgInsertTime = sum(iTime) / len(iTime) if iTime else 0
        avgSearchTime = sum(sTime) / len(sTime) if sTime else 0
        avgInsertHop = iHops / nSize if nSize else 0
        avgSearchHops = sHops / nSize if nSize else 0

        totalActions = nSize * 2 + deleteAmount
        totalErrs = iError + sError + deleteErrors
        errorPersentage = (totalErrs / totalActions) * 100

        results_data.append(
            {
                "Batch Size": nSize,
                "Avg Insert Time (s)": round(avgInsertTime, 5),
                "Avg Search Time (s)": round(avgSearchTime, 5),
                "Avg Insert Hops": round(avgInsertHop, 2),
                "Avg Search Hops": round(avgSearchHops, 2),
                "Error Rate (%)": round(errorPersentage, 2),
            }
        )

        n.append(nSize)
        avgInsetTime.append(avgInsertTime)
        avgSearchTime.append(avgSearchTime)
        avgInsertHops.append(avgInsertHop)
        avgSearchHops.append(avgSearchHops)
        errRate.append(errorPersentage)

    csv_file = os.path.join(RESUTL_DIR, "simulation_results.csv")
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results_data[0].keys())
        writer.writeheader()
        writer.writerows(results_data)

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].plot(n, avgInsertHops, label="Insert Hops", marker="o", color="blue")
    axs[0].plot(n, avgSearchHops, label="Search Hops", marker="x", color="cyan")
    axs[0].set_title("Average Network Hops vs Batch Size")
    axs[0].set_xlabel("Batch Size (Operations)")
    axs[0].set_ylabel("Average Hops")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(n, avgInsetTime, label="Insert Time (s)", marker="o", color="red")
    axs[1].plot(n, avgSearchTime, label="Search Time (s)", marker="x", color="orange")
    axs[1].set_title("Average Operation Latency vs Batch Size")
    axs[1].set_xlabel("Batch Size (Operations)")
    axs[1].set_ylabel("Time (Seconds)")
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(n, errRate, label="Error Rate (%)", marker="s", color="green")
    axs[2].set_title("Error Rate vs Batch Size")
    axs[2].set_xlabel("Batch Size (Operations)")
    axs[2].set_ylabel("Error Rate (%)")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()

    png_file = os.path.join(RESUTL_DIR, "simulation_graphs.png")
    plt.savefig(png_file)
    print(f"Data saved to {csv_file}")
    print(f"Graphs saved to {png_file}")


if __name__ == "__main__":
    run_simulation()
