"""Print a one-time snapshot of system resource usage."""
from __future__ import annotations

import argparse
import shutil


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=float, default=1.0,
                        help="CPU sampling interval in seconds")
    args = parser.parse_args()

    try:
        import psutil
    except ImportError as exc:
        raise SystemExit("Install dependencies with: python -m pip install -r requirements.txt") from exc

    if args.interval < 0:
        parser.error("--interval cannot be negative")

    cpu = psutil.cpu_percent(interval=args.interval)
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")
    network = psutil.net_io_counters()

    print(f"CPU usage:       {cpu:.1f}%")
    print(f"Memory usage:    {memory.percent:.1f}% "
          f"({memory.used / 2**30:.2f} / {memory.total / 2**30:.2f} GiB)")
    print(f"Disk usage (/):  {disk.used / disk.total * 100:.1f}% "
          f"({disk.used / 2**30:.2f} / {disk.total / 2**30:.2f} GiB)")
    print(f"Network sent:    {network.bytes_sent / 2**20:.2f} MiB")
    print(f"Network received:{network.bytes_recv / 2**20:.2f} MiB")


if __name__ == "__main__":
    main()
