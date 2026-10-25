from processor import CommandProcessor


def main() -> None:
    processor = CommandProcessor()
    processor.process_file("commands.txt")


if __name__ == "__main__":
    main()
