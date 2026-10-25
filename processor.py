import shlex

from models import MusicalWork, Song, Symphony


class CommandProcessor:
    """Обрабатывает файл команд и хранит музыкальные произведения."""

    def __init__(self) -> None:
        self.works: list[MusicalWork] = []

    def process_add(self, arguments: str) -> None:
        try:
            parts = shlex.split(arguments)
        except ValueError as error:
            print(f"Ошибка синтаксиса ADD: {error}")
            return

        try:
            if len(parts) != 4:
                print(f"Ошибка команды ADD: {arguments}")
                return

            work_type = parts[0]
            name = parts[1]
            duration = float(parts[2])
            author = parts[3]

            if work_type == "SONG":
                work = Song(name, duration, author)
            elif work_type == "SYMPHONY":
                work = Symphony(name, duration, author)
            else:
                print(f"Неизвестный тип произведения: {work_type}")
                return

            self.works.append(work)
            print(f'Добавлено: "{name}"')

        except ValueError:
            print("Ошибка: длительность должна быть числом.")

    def process_remove(self, arguments: str) -> None:
        try:
            parts = shlex.split(arguments)
        except ValueError as error:
            print(f"Ошибка синтаксиса REM: {error}")
            return

        if len(parts) != 3:
            print(f"Ошибка команды REM: {arguments}")
            return

        field = parts[0]
        operator = parts[1]
        value = parts[2]

        old_count = len(self.works)

        self.works = [
            work
            for work in self.works
            if not work.matches(field, operator, value)
        ]

        removed_count = old_count - len(self.works)
        print(f"Удалено объектов: {removed_count}")

    def process_print(self) -> None:
        print()
        print("========== МУЗЫКАЛЬНЫЕ ПРОИЗВЕДЕНИЯ ==========")

        if not self.works:
            print("Контейнер пуст.")
        else:
            for index, work in enumerate(self.works, start=1):
                print()
                print(f"Объект №{index}")
                print("-" * 35)
                work.print_info()

        print()
        print("=" * 49)

    def process_command(self, line: str) -> None:
        line = line.strip()

        if not line or line.startswith("#"):
            return

        if line.startswith("ADD "):
            self.process_add(line[4:])
        elif line.startswith("REM "):
            self.process_remove(line[4:])
        elif line == "PRINT":
            self.process_print()
        else:
            print(f"Неизвестная команда: {line}")

    def process_file(self, filename: str) -> None:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    self.process_command(line)
        except FileNotFoundError:
            print(f'Файл "{filename}" не найден.')
