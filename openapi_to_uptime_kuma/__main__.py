import yaml
import argparse
from .parser import extract_monitor_entries
from .client import upsert_monitors

def main():
    parser = argparse.ArgumentParser(description="Process some configuration parameters.")

    parser.add_argument('--spec', required=True, type=str, help='Path to the spec file (e.g., spec.yaml)')
    parser.add_argument('--service', required=True, type=str, help='Service name (e.g., service1)')

    args = parser.parse_args()
    
    with open(args.spec, 'r') as file:
        data = yaml.safe_load(file)
    entries = extract_monitor_entries(data)
    upsert_monitors(args.service, entries)

if __name__ == "__main__":
    main()
