import json


def generate_metrics(nodes_file_path):
    # Load nodes data from file
    with open(nodes_file_path, "r") as file:
        nodes_data = json.load(file)

    # Iterate through each node and generate metrics
    for node in nodes_data.get("nodes", []):
        node_name = node.get("node_name")

        # Define the required metrics template for each node
        metrics = {
            "storage": {
                "disks": [],
                "blocksizes": ["4k", "16k", "128k", "1M", "10M", "100M"],
                "workloads": ["seqwr", "seqrd", "seqrewr", "rndwr", "rndrd", "rndrw"],
                "threads": [4, 8, 16, 32, 64],
                "flags": [{
                    "file-extra-flags": "dsync"
                }]
            },
            "network": {
                "interfaces": [],
                "threads": [1, 4, 16, 64],
                "peers": [],
                "workloads": ["iperf", "ping", "hping3"]
            },
            "cpu": {
                "parameters": [{
                    "threads": [1, 2, 4, 8, 16, 32, 64, 128, 256],
                    "cpu-max-prime": 100000
                }]
            }
        }

        # Extract disk and network interface information for the current node
        metrics["storage"]["disks"] = [{"path": disk}
                                       for disk in node.get("disks", [])]
        metrics["network"]["interfaces"] = node.get("network_interfaces", [])

        # Set peers as all other nodes except the current node
        metrics["network"]["peers"] = [
            other_node.get("node_name")
            for other_node in nodes_data.get("nodes", [])
            if other_node.get("node_name") != node_name
        ]

        # Save metrics to output file for each node
        output_file_path = f"{node_name}_metrics.json"
        with open(output_file_path, "w") as file:
            json.dump(metrics, file, indent=4)


# Usage Example
if __name__ == "__main__":
    generate_metrics("node_info.json")
