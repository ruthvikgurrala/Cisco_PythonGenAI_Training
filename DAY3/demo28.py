from pathlib import Path
import pprint


def main() -> None:
    cfg_path = Path(__file__).parent / "network.cfg"
    out_path = Path(__file__).parent / "new_network.cfg"

    network_params: dict[str, object] = {}

    with open(cfg_path, "r") as fobj:
        for line in fobj.readlines():
            line = line.strip()
            if line and "=" in line:
                key, val = line.split("=")
                network_params[key] = val

    print("Initial Network Configuration:")
    pprint.pprint(network_params)

    # Update parameters
    network_params["Interface"] = "eth1"
    network_params["bootproto"] = "static"
    network_params["onboot"] = "yes"
    network_params["IPADD"] = "192.168.1.10"
    network_params["PREFIX"] = 24
    network_params["DNS1"] = "122.33.344.555"

    print("\nUpdated Dict details:-")
    pprint.pprint(network_params)

    with open(out_path, "w") as wobj:
        for key, val in network_params.items():
            wobj.write(f"{key} = {val}\n")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates reading and parsing INI/key-value style configuration files into a dictionary,
mutating dictionary entries, and writing the updated key-value mappings back to a new configuration file.
"""
