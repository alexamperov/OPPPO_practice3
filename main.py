"""Точка входа в приложение «Музыкальные произведения» (вариант 18)."""

from pathlib import Path

from processor import CommandProcessor


def main() -> None:
    """Запустить чтение команд рядом с исходным кодом программы."""
    commands_path = Path(__file__).with_name("commands.txt")
    processor = CommandProcessor()
    processor.process_file(str(commands_path))


if __name__ == "__main__":
    main()
