import argparse

import yaml

from src.main import Application


def main():
    parser = argparse.ArgumentParser(
        description="Process input files using ReadManager, SplitManager, and ChunkManager \
            to produce chunks."
    )
    parser.add_argument(
        "config_file",
        nargs="?",
        default="config.yaml",
        help="Path to the YAML configuration file (default: config.yaml)",
    )
    args = parser.parse_args()

    # Load configuration once.
    try:
        with open(args.config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return

    # Create and run the application.
    app = Application(config)
    app.run()


if __name__ == "__main__":
    main()
