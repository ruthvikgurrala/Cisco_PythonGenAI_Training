from pathlib import Path
import time


def main() -> None:
    output_path = Path(__file__).parent / "r2.log"

    devices: list[str] = ["switches", "routers", "ethernet", "rs232"]
    config: dict[str, object] = {
        "ID": "A-123",
        "app": "demoApp",
        "port": 3030,
        "fname": "/etc/app.cfg",
    }

    wobj = open(output_path, "w")

    for device in devices:
        wobj.write(f"Device name:{device}\n")

    wobj.write("---- done -----\n")

    for key, value in config.items():
        wobj.write(f"{key} = {value}\n")

    wobj.write("-------- Done -------\n")
    wobj.write(f"Created on {time.ctime()}\n")
    wobj.close()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates writing data from both list and dictionary collections into a file,
iterating dictionary key-value pairs, and appending system timestamps using time.ctime().
"""