from pathlib import Path
import pprint

BASE_DIR = Path(__file__).parent


def f1() -> dict:
    """Return an empty dictionary for configuration storage."""
    return {}


def f2(network_params: dict) -> dict:
    """
    Read 'network.cfg' and populate configuration key-value pairs into the dictionary.
    """
    cfg_path = BASE_DIR / "network.cfg"
    with open(cfg_path, "r") as fobj:
        for line in fobj.readlines():
            line = line.strip()
            if line and "=" in line:
                key, val = line.split("=")
                network_params[key] = val
    return network_params


def f3(network_params: dict) -> None:
    """Display current network configuration parameters using pprint."""
    pprint.pprint(network_params)


def f4(network_params: dict) -> dict:
    """Apply updated static network parameters to the configuration dictionary."""
    network_params["Interface"] = "eth1"
    network_params["bootproto"] = "static"
    network_params["onboot"] = "yes"
    network_params["IPADD"] = "192.168.1.10"
    network_params["PREFIX"] = 24
    network_params["DNS1"] = "122.33.344.555"
    return network_params


def f5(network_params: dict) -> None:
    """Write the updated configuration dictionary to 'new_network.cfg'."""
    out_path = BASE_DIR / "new_network.cfg"
    with open(out_path, "w") as wobj:
        for key, val in network_params.items():
            wobj.write(f"{key} = {val}\n")


def main() -> None:
    config = f1()
    config = f2(config)
    f3(config)
    config = f4(config)
    print("\nUpdated network details:-")
    f3(config)
    f5(config)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates Python best practices with formal function docstrings, modular function decomposition,
dictionary parameter mutation, and structured pipeline orchestration through a main entry point.
"""