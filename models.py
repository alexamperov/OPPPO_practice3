from abc import ABC, abstractmethod
from operator import eq, ge, gt, le, lt, ne


class MusicalWork(ABC):
    """Базовый класс для музыкальных произведений."""

    def __init__(self, name: str, duration: float) -> None:
        self.name = name
        self.duration = duration

    @abstractmethod
    def get_type(self) -> str:
        """Возвращает тип произведения."""
        pass

    @abstractmethod
    def get_author(self) -> str:
        """Возвращает исполнителя или композитора."""
        pass

    @abstractmethod
    def get_author_role(self) -> str:
        """Возвращает подпись роли автора."""
        pass

    def print_info(self) -> None:
        print(f"Тип: {self.get_type()}")
        print(f"Название: {self.name}")
        print(f"Длительность: {self.duration} мин.")
        print(f"{self.get_author_role()}: {self.get_author()}")

    def matches(self, field: str, operator: str, value: str) -> bool:
        """Проверяет, подходит ли объект под условие команды REM."""

        if field == "duration":
            try:
                reference = float(value)
            except ValueError:
                return False

            comparisons = {
                ">": gt,
                "<": lt,
                ">=": ge,
                "<=": le,
                "==": eq,
                "!=": ne,
            }
            comparison = comparisons.get(operator)
            return comparison(self.duration, reference) if comparison else False

        text_values = {
            "name": self.name,
            "author": self.get_author(),
            "type": self.get_type(),
        }
        if field not in text_values:
            return False
        if operator == "==":
            return text_values[field] == value
        if operator == "!=":
            return text_values[field] != value
        return False



class Song(MusicalWork):
    """Песня. Уникальный параметр - исполнитель."""

    def __init__(self, name: str, duration: float, performer: str) -> None:
        super().__init__(name, duration)
        self.performer = performer

    def get_type(self) -> str:
        return "SONG"

    def get_author(self) -> str:
        return self.performer

    def get_author_role(self) -> str:
        return "Исполнитель"


class Symphony(MusicalWork):
    """Симфония. Уникальный параметр - композитор."""

    def __init__(self, name: str, duration: float, composer: str) -> None:
        super().__init__(name, duration)
        self.composer = composer

    def get_type(self) -> str:
        return "SYMPHONY"

    def get_author(self) -> str:
        return self.composer

    def get_author_role(self) -> str:
        return "Композитор"
