import argparse

from app import NewsApp


def main():
    parser = argparse.ArgumentParser(description="NewsTerminal TUI")
    parser.add_argument("--config", default="configs/configs.yaml")
    args = parser.parse_args()

    app = NewsApp(config_path=args.config)
    app.run()


if __name__ == "__main__":
    main()