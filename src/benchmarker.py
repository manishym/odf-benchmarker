from network_benchmarker import NetworkBenchmarker
from cpu_benchmarker import CPUBenchmarker
from storage_benchmarker import StorageBenchmarker
from metrics_generator import generate_metrics
import pandas as pd
import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description="Run various benchmarks on the system.")
    parser.add_argument("--config", type=str, required=True,
                        help="Path to the configuration file.")
    args = parser.parse_args()
    with open(args.config) as f:
        config = json.load(f)
        config = generate_metrics(config)
    print("Running benchmarks with the following configuration:")
    cpu = CPUBenchmarker(config.get("cpu", {}))
    storage = StorageBenchmarker(config.get(
        "storage", {})) if config.get("storage", {}) else None
    network = NetworkBenchmarker(config.get("network", {}))
    df = pd.DataFrame()
    for b in [cpu, storage, network]:
        print("Running", b.__class__.__name__)
        if b is None:
            continue
        bdf = b.run()
        df = pd.concat([df, bdf])
    df.to_csv("results.csv", index=False)
    print(df)


if __name__ == "__main__":
    main()
