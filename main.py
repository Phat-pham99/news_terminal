import argparse
import os
from pathlib import Path

from app import NewsApp


def main():
    parser = argparse.ArgumentParser(description="NewsTerminal TUI")
    parser.add_argument("--config", default="configs/configs.yaml")
    args = parser.parse_args()

    project_root = Path(__file__).parent
    config_path = project_root / args.config if not os.path.isabs(args.config) else Path(args.config)

    app = NewsApp(config_path=str(config_path))
    app.run()


if __name__ == "__main__":
    main()