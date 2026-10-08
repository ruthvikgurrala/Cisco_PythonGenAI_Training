from pathlib import Path
import pprint

BASE_DIR = Path(__file__).parent


def f1() -> dict:
    """Return an empty configuration dictionary."""
    return {}


def f2(network_params: dict) -> dict:
    """Read network.cfg and populate the configuration dictionary."""
    cfg_path = BASE_DIR / "network.cfg"
    with open(cfg_path, "r") as fobj:
        for line in fobj.readlines():
            line = line.strip()
            if line and "=" in line:
                key, val = line.split("=")
                network_params[key] = val
    return network_params


def f3(network_params: dict) -> None:
    """Display network parameters."""
    pprint.pprint(network_params)


def f4(network_params: dict) -> dict:
    """Update network parameters."""
    network_params["Interface"] = "eth1"
    network_params["bootproto"] = "static"
    network_params["onboot"] = "yes"
    network_params["IPADD"] = "192.168.1.10"
    network_params["PREFIX"] = 24
    network_params["DNS1"] = "122.33.344.555"
    return network_params


def f5(network_params: dict) -> None:
    """Write updated configuration dictionary to new_network.cfg."""
    out_path = BASE_DIR / "new_network.cfg"
    with open(out_path, "w") as wobj:
        for key, val in network_params.items():
            wobj.write(f"{key} = {val}\n")


def main() -> None:
    rv1 = f1()
    rv2 = f2(rv1)
    f3(rv2)
    rv3 = f4(rv2)
    print("\nUpdated network details:-")
    f3(rv3)
    f5(rv3)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates refactoring procedural code into single-responsibility functions (f1 through f5),
passing state between functions via arguments and return values, and managing file I/O within modules.
"""